"""
Implement a task scheduler in Python that uses a custom-built priority queue
based on a binary heap. Each task is represented as a tuple (priority, task_id),
where a lower numerical value means a higher priority. In addition to standard
operations, your priority queue should support updating the priority of a given
task.

Requirements
- Each task is stored as a tuple (priority, task_id).
- Operations to Implement:
    - insert(priority, task_id): Add a new task.
    - peek(): Return the task with the highest priority (lowest number) without removing it.
    - extract_min(): Remove and return the task with the highest priority.
    - update(task_id, new_priority): Update the priority of a task that already exists and adjust the heap accordingly.
"""

from dataclasses import dataclass
from heapq import heappush, heappop, heapify


@dataclass(frozen=True)
class Task:
    priority: int
    task_id: int
    description: str = ""
    duration: float = 0.0

    def __str__(self):
        return f"<{self.task_id}, {self.priority}, {self.description}>"

    def __lt__(self, other):
        return self.priority < other.priority


class TaskScheduler:
    def __init__(self):
        self.heap = []
        self.task_index = {}

    def insert(self, task: Task):
        """
        Add a new task to the priority queue.
        """
        if task.task_id in self.task_index:
            raise ValueError("Task with this ID already exists.")
        heappush(self.heap, task)
        self.task_index[task.task_id] = self.heap.index(task)

    def peek(self) -> Task | None:
        """
        Return the task with the highest priority without removing it.
        """
        return self.heap[0] if self.heap else None

    def pop(self) -> Task | None:
        """
        Remove and return the task with the highest priority.
        """
        if not self.heap:
            return None
        task = heappop(self.heap)
        del self.task_index[task.task_id]
        return task

    def update(self, task_id: int, new_priority: int):
        """
        Update the priority of a task that already exists and adjust the heap accordingly.
        """
        if task_id not in self.task_index:
            raise ValueError("Task with this ID does not exist.")
        index = self.task_index[task_id]
        old_task = self.heap[index]
        new_task = Task(new_priority, task_id, old_task.description, old_task.duration)
        self.heap[index] = new_task
        heapify(self.heap)
        self.task_index[task_id] = self.heap.index(new_task)

    def __iter__(self):
        """
        Return the tasks in order of priority without removing them.
        """
        stack = [0]
        while stack:
            current = stack.pop()
            yield self.heap[current]
            if current * 2 + 1 < len(self.heap):
                stack.append(current * 2 + 1)
            if current * 2 + 2 < len(self.heap):
                stack.append(current * 2 + 2)

    def estimated_time_to_start(self, task_id: int) -> float:
        """
        Estimate the time remaining to start a specific task
        """
        eta = 0
        for task in self:
            if task.task_id != task_id:
                eta += task.duration
            else:
                break
        return eta
