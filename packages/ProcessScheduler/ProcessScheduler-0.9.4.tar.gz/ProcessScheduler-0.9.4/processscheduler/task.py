"""The module that defines the task related classes."""

# Copyright (c) 2020-2021 Thomas Paviot (tpaviot@gmail.com)
#
# This file is part of ProcessScheduler.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from typing import List, Optional

from z3 import And, ArithRef, Bool, BoolRef, If, Int, Or

from processscheduler.base import _NamedUIDObject
from processscheduler.util import (
    is_strict_positive_integer,
    is_positive_integer,
    is_list_of_positive_integers,
)
from processscheduler.resource import Resource, Worker, CumulativeWorker, SelectWorkers
import processscheduler.context as ps_context


class Task(_NamedUIDObject):
    """a Task object"""

    def __init__(self, name: str, optional: bool = False) -> None:
        super().__init__(name)
        self.work_amount = 0
        self.priority = 1  # by default

        # workers required to process the task
        self.required_resources = []  # type: List[Resource]
        # the following list is used for json export only
        # it stores the parameter passed to the add_required_resource
        # method
        self.required_resources_names = []  # type: List[str]

        # z3 Int variables
        self.start = Int(f"{name}_start")  # type: ArithRef
        self.end = Int(f"{name}_end")  # type: ArithRef
        self.duration = Int(f"{name}_duration")  # type: ArithRef

        # by default, the task is mandatory
        self.scheduled = True  # type: Union[bool, BoolRef]

        # but it can be se as optional. In that case, the self.scheduled
        # above flag will be overridden as a z3 BoolRef
        self.optional = optional  # type: bool

        # add this task to the current context
        if ps_context.main_context is None:
            raise AssertionError(
                "No context available. First create a SchedulingProblem"
            )
        # the task_number is an integer that is incremented each time
        # a task is created. The first task has number 1, the second number 2 etc.
        self.task_number = ps_context.main_context.add_task(self)  # type: int

        # the counter used for negative integers
        # negative integers are used to schedule optional tasks
        # for such tasks, they are actually scheduled in the past
        # with start_time = end_time is a negative point in the timeline
        self._current_negative_integer = 0  # type: int

    def _get_unique_negative_integer(self) -> int:
        """Returns a new negative integer each time this method is called."""
        self._current_negative_integer -= 1  # decrement the current counter
        return self._current_negative_integer

    def add_required_resource(self, resource: Resource, dynamic=False) -> None:
        """
        Add a required resource to the current task.

        Args:
            resource: any of one of the Resource derivatives class (Worker, SelectWorkers etc.)
        If dynamic flag (False by default) is set to True, then the resource is dynamic
        and can join the task any time between its start and end times.
        """
        if not isinstance(resource, Resource):
            raise TypeError("you must pass a Resource instance")

        if resource in self.required_resources:
            raise ValueError(
                f"resource {resource.name} already defined as a required resource for task {self.name}"
            )

        # store the resource name
        self.required_resources_names.append(resource.name)

        if isinstance(resource, CumulativeWorker):
            # in the case for a CumulativeWorker, select at least one worker
            resource = resource.get_select_workers()

        if isinstance(resource, SelectWorkers):
            # loop over each resource
            for worker in resource.list_of_workers:
                resource_maybe_busy_start = Int(
                    f"{worker.name}_maybe_busy_{self.name}_start"
                )
                resource_maybe_busy_end = Int(
                    f"{worker.name}_maybe_busy_{self.name}_end"
                )
                # create the busy interval for the resource
                worker.add_busy_interval(
                    self, (resource_maybe_busy_start, resource_maybe_busy_end)
                )
                # add assertions. If worker is selected then sync the resource with the task
                selected_variable = resource.selection_dict[worker]
                schedule_as_usual = And(
                    resource_maybe_busy_start == self.start,
                    resource_maybe_busy_end == self.end,
                )
                # in the case the worker is selected
                # move the busy interval to a single point in time, in the
                # past. This way, it does not conflict with tasks to be
                # actuallt scheduled.
                # This single point in time results in a zero duration time: related
                # task will not be considered when cimputing resource utilization or cost.
                single_point_in_past = self._get_unique_negative_integer()
                move_to_past = And(
                    resource_maybe_busy_start == single_point_in_past,  # to past
                    resource_maybe_busy_end == single_point_in_past,
                )
                # define the assertion ...
                assertion = If(selected_variable, schedule_as_usual, move_to_past)
                # ... and store it into the task assertions list
                self.append_z3_assertion(assertion)
                # finally, add each worker to the "required" resource list
                self.required_resources.append(worker)
            # also, don't forget to add the AlternativeWorker assertion
            self.append_z3_assertion(resource.selection_assertion)
        elif isinstance(resource, Worker):
            resource_busy_start = Int(f"{resource.name}_busy_{self.name}_start")
            resource_busy_end = Int(f"{resource.name}_busy_{self.name}_end")
            # create the busy interval for the resource
            resource.add_busy_interval(self, (resource_busy_start, resource_busy_end))
            # set the busy resource to keep synced with the task
            if dynamic:
                self.append_z3_assertion(resource_busy_end <= self.end)
                self.append_z3_assertion(resource_busy_start >= self.start)
            else:
                # self.append_z3_assertion(resource_busy_start + self.duration == resource_busy_end)
                self.append_z3_assertion(resource_busy_end == self.end)
                self.append_z3_assertion(resource_busy_start == self.start)
            # finally, store this resource into the resource list
            self.required_resources.append(resource)

    def add_required_resources(
        self, list_of_resources: List[Resource], dynamic=False
    ) -> None:
        """
        Add a set of required resources to the current task.

        This method calls the add_required_resource method for each resource of the list.
        As a consequence, be aware this is not an atomic transaction.

        Args:
            list_of_resources: the list of resources to add.
        """
        for resource in list_of_resources:
            self.add_required_resource(resource, dynamic)

    def set_assertions(self, list_of_z3_assertions: List[BoolRef]) -> None:
        """Take a list of constraint to satisfy. Create two cases: if the task is scheduled,
        nothing is done; if the task is optional, move task to the past"""
        if self.optional:  # in this case the previous assertions maybe skipped
            self.scheduled = Bool(f"{self.name}_scheduled")
            # the first task is moved to -1, the second to -2
            # etc.
            point_in_past = -self.task_number
            not_scheduled_assertion = And(
                self.start == point_in_past,  # to past
                self.end == point_in_past,  # to past
                self.duration == 0,
            )
            self.append_z3_assertion(
                If(self.scheduled, And(list_of_z3_assertions), not_scheduled_assertion)
            )
        else:
            self.append_z3_assertion(And(list_of_z3_assertions))


class ZeroDurationTask(Task):
    """Task with zero duration, an instant in the schedule.

    The task end and start are constrained to be equal.

    Args:
        name: the task name. It must be unique
    """

    def __init__(self, name: str, optional: Optional[bool] = False) -> None:
        super().__init__(name, optional)
        # add an assertion: end = start because the duration is zero
        assertions = [self.start == self.end, self.duration == 0]

        self.set_assertions(assertions)


class FixedDurationTask(Task):
    """Task with constant duration.

    Args:
        name: the task name. It must be unique
        duration: the task duration as a number of periods
        work_amount: represent the quantity of work this task must produce
        priority: the task priority. The greater the priority, the sooner it will be scheduled
        optional: True if task schedule is optional, False otherwise (default)
    """

    def __init__(
        self,
        name: str,
        duration: int,
        work_amount: Optional[int] = 0,
        priority: Optional[int] = 1,
        optional: Optional[bool] = False,
    ) -> None:
        super().__init__(name, optional)
        if not is_strict_positive_integer(duration):
            raise TypeError("duration must be a strict positive integer")
        self.duration_defined_value = duration

        if not is_positive_integer(work_amount):
            raise TypeError("work_amount me be a positive integer")
        self.work_amount = work_amount

        if not is_positive_integer(work_amount):
            raise TypeError("work_amount me be a positive integer")
        self.priority = priority

        assertions = [
            self.start + self.duration == self.end,
            self.duration == duration,
            self.start >= 0,
        ]

        self.set_assertions(assertions)


class UnavailabilityTask(FixedDurationTask):
    """A task that tells that a resource is unavailable during this period. This
    task is not publicly exposed, it is used by the resource constraint
    ResourceUnavailability.
    """

    def __init__(self, name: str, duration: int) -> None:
        super().__init__(name, duration, work_amount=0, priority=0)


class VariableDurationTask(Task):
    """The duration can take any value, computed by the solver."""

    def __init__(
        self,
        name: str,
        min_duration: Optional[int] = 0,
        max_duration: Optional[int] = None,
        allowed_durations: Optional[List[int]] = None,
        work_amount: Optional[int] = 0,
        priority: Optional[int] = 1,
        optional: Optional[bool] = False,
    ):
        super().__init__(name, optional)

        # allowed durations and min/max are exclusive
        if is_list_of_positive_integers(allowed_durations):
            all_cstr = [self.duration == duration for duration in allowed_durations]
            self.append_z3_assertion(Or(all_cstr))
        else:
            if is_positive_integer(max_duration):
                self.append_z3_assertion(self.duration <= max_duration)
            elif max_duration is not None:
                raise TypeError(
                    "length_as_most should either be a positive integer or None"
                )

            if not is_positive_integer(min_duration):
                raise TypeError("min_duration must be a positive integer")

            if not is_positive_integer(work_amount):
                raise TypeError("work_amount must be a positive integer")

        self.min_duration = min_duration
        self.max_duration = max_duration
        self.allowed_durations = allowed_durations
        self.work_amount = work_amount
        self.priority = priority

        assertions = [
            self.start + self.duration == self.end,
            self.start >= 0,
            self.duration >= min_duration,
        ]

        if max_duration is not None:
            assertions.append(self.duration <= max_duration)

        if min_duration is not None:
            assertions.append(self.duration >= min_duration)

        self.set_assertions(assertions)
