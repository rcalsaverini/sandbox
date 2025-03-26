import pytest
from hypothesis import given, strategies as st
from examples.p04 import reverse_linked_list, llist

functions = [reverse_linked_list]


@st.composite
def create_case(draw) -> tuple[list[int], list[int]]:
    """
    generate two linked lists which are the inverted form of each other
    """
    array = draw(st.lists(st.integers(min_value=0, max_value=100), min_size=2))
    inverted_array = array[::-1]
    return llist.from_list(array), llist.from_list(inverted_array)


@given(create_case())
@pytest.mark.parametrize("function", functions)
def test_cases(function, case):
    d_list, i_list = case
    assert function(d_list) == i_list


@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1))
@pytest.mark.parametrize("function", functions)
def test_is_own_inverse(function, array):
    d_list = llist.from_list(array)
    assert function(function(d_list)) == d_list
