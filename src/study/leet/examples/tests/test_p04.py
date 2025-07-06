import pytest
from hypothesis import given, strategies as st
from examples.p04 import (
    reverse_linked_list,
    detect_cycle,
    merge_sorted_lists,
    llist,
    merge_multiple_sorted_lists,
    merge_multiple_sorted_lists_non_recursive,
)


@st.composite
def inverted_llists(draw) -> tuple[list[int], list[int]]:
    """
    generate two linked lists which are the inverted form of each other
    """
    array = draw(st.lists(st.integers(min_value=0, max_value=100), min_size=2))
    inverted_array = array[::-1]
    return llist.from_list(array), llist.from_list(inverted_array)


@st.composite
def llists_no_cycle(draw) -> llist:
    st_values = st.integers(min_value=0, max_value=100)
    array = draw(st.lists(st_values, min_size=1, unique=True))
    return llist.from_list(array)


@st.composite
def llists_with_cycle(draw) -> llist:
    st_values = st.integers(min_value=0, max_value=100)
    first, second, *rest = draw(st.lists(st_values, min_size=3, unique=True))
    loop_point = draw(st.integers(0, len(rest) - 1))
    tail = llist(first)
    output = llist(second, tail)
    for i, x in enumerate(rest):
        output = llist(x, output)
        if i == loop_point:
            tail.next = output
    return output


@given(inverted_llists())
def test_cases(case):
    d_list, i_list = case
    assert reverse_linked_list(d_list) == i_list


@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1))
def test_is_own_inverse(array):
    d_list = llist.from_list(array)
    assert reverse_linked_list(reverse_linked_list(d_list)) == d_list


@given(llists_no_cycle())
def test_detect_cycle_no_cycle(head):
    assert not detect_cycle(head)


@given(llists_with_cycle())
def test_detect_cycle_with_cycle(head):
    assert detect_cycle(head)


st_list = st.lists(st.integers(min_value=0, max_value=100), min_size=1)


@given(st_list, st_list)
def test_merge_sorted_lists(array1, array2):
    llist1 = llist.from_list(sorted(array1))
    llist2 = llist.from_list(sorted(array2))
    expected = list(sorted(array1 + array2))
    assert merge_sorted_lists(llist1, llist2).to_list() == expected


@given(st.lists(st_list))
def test_merge_multiple_sorted_lists(arrays):
    lists = [llist.from_list(sorted(array)) for array in arrays]
    expected = list(sorted([x for array in arrays for x in array]))
    if not lists:
        assert merge_multiple_sorted_lists(lists) is None
    else:
        assert merge_multiple_sorted_lists(lists).to_list() == expected


merge_multiple_sorted_lists_non_recursive


@given(st.lists(st_list))
def test_merge_multiple_sorted_lists_non_recursive(arrays):
    lists = [llist.from_list(sorted(array)) for array in arrays]
    expected = list(sorted([x for array in arrays for x in array]))
    if not lists:
        assert merge_multiple_sorted_lists_non_recursive(lists) is None
    else:
        assert merge_multiple_sorted_lists_non_recursive(lists).to_list() == expected
