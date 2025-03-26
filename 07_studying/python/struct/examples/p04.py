# Given a linked list, the task is to reverse the linked list by changing the links between nodes.

# Examples:

# Input: head: 1 -> 2 -> 3 -> 4 -> NULL
# Output: head: 4 -> 3 -> 2 -> 1 -> NULL
# Explanation: Reversed Linked List:

from dataclasses import dataclass


@dataclass
class llist:
    data: int
    next: "llist" = None

    @classmethod
    def from_list(cls, data: list[int]) -> "llist":
        head = None
        for i in reversed(data):
            head = cls(i, head)
        return head


def reverse_linked_list(head: llist) -> llist:
    pass
