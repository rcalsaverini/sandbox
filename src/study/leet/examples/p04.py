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

    def to_list(self) -> list[int]:
        output = []
        while self:
            output.append(self.data)
            self = self.next
        return output


def reverse_linked_list(head: llist) -> llist:
    reversed = None
    while head:
        reversed = llist(head.data, reversed)
        head = head.next
    return reversed


def detect_cycle(head: llist) -> bool:
    seen = set()
    while head:
        if head.data in seen:
            return True
        seen.add(head.data)
        head = head.next
    return False


def merge_sorted_lists(l1: llist, l2: llist) -> llist:
    dummy = llist(None)
    curr = dummy
    while l1 and l2:
        if l1.data < l2.data:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    if l1:
        curr.next = l1
    else:
        curr.next = l2
    return dummy.next


def merge_multiple_sorted_lists(lists: list[llist]) -> llist:
    if not lists:
        return None
    if len(lists) == 1:
        return lists[0]
    if len(lists) == 2:
        return merge_sorted_lists(lists[0], lists[1])
    first, second, *rest = lists
    return merge_multiple_sorted_lists([merge_sorted_lists(first, second)] + rest)


def merge_multiple_sorted_lists_non_recursive(lists: list[llist]) -> llist:
    if not lists:
        return None
    if len(lists) == 1:
        return lists[0]
    dummy = llist(None)
    curr = dummy
    while any([ll is not None for ll in lists]):
        index_smallest = min(range(len(lists)), key=lambda i: lists[i].data)
        curr.next = lists[index_smallest]
        lists[index_smallest] = lists[index_smallest].next
        if not lists[index_smallest]:
            lists.pop(index_smallest)
        curr = curr.next
    for ll in lists:
        if ll:
            curr.next = ll
            break
    return dummy.next
