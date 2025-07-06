"""
Test cases for p05.py
Exercises involving stacks
"""

from hypothesis import given, strategies as st
from examples.p06 import TaskScheduler, Task
from numpy import cumsum


@st.composite
def st_case(draw) -> list[Task]:
    """
    Generate a pair of infix and postfix expressions
    Ex.: ('a+b', 'ab+')
    """
    st_priority = st.integers(min_value=1, max_value=10)
    st_duration = st.floats(min_value=0.0, max_value=1.0)
    priorities = draw(
        st.lists(st_priority, min_size=3, unique=True, max_size=10),
    )

    return [
        Task(priority, k, "", draw(st_duration))
        for k, priority in enumerate(priorities)
    ]


@given(st_case())
def test_corrent_order(tasks):
    expected_order = [task.task_id for task in sorted(tasks)]
    scheduler = TaskScheduler()
    for task in tasks:
        scheduler.insert(task)
    while scheduler.peek():
        task = scheduler.pop()
        assert task.task_id == expected_order.pop(0)


@given(st_case())
def test_correct_times(tasks):
    expected_times = {
        task.task_id: sum(
            other.duration for other in tasks if other.priority > task.priority
        )
        for task in tasks
    }

    scheduler = TaskScheduler()
    for task in tasks:
        scheduler.insert(task)
    for task_id, expected_time in expected_times.items():
        scheduler.estimated_time_to_start(task_id) == expected_time
