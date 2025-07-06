import pytest
from hypothesis import given, example, strategies as st
from numpy import random as rnd
from examples.p01 import (
    two_sum_brute_force,
    two_sum_pointers,
    two_sum_hash,
    two_sum_binary_search,
)

functions = [two_sum_brute_force, two_sum_pointers, two_sum_hash, two_sum_binary_search]


@st.composite
def true_case(draw):
    arr = draw(st.lists(st.integers(), min_size=2, max_size=100))
    i = rnd.randint(0, len(arr))
    while True:
        j = rnd.randint(0, len(arr))
        if i != j:
            break
    return (arr, arr[i] + arr[j])


@st.composite
def false_case(draw):
    arr = draw(st.lists(st.integers(), min_size=2, max_size=100))
    all_sums = {
        arr[i] + arr[j]
        for i in range(len(arr))
        for j in range(i + 1, len(arr))
        if i != j
    }
    while True:
        target = rnd.randint(-10, 10)
        if target not in all_sums:
            return (arr, target)


@given(true_case())
@pytest.mark.parametrize("function", functions)
def test_true_cases(function, case):
    array, target = case
    assert function(array, target)


@given(false_case())
@example(([0, 1], 2))
@pytest.mark.parametrize("function", functions)
def test_false_cases(function, case):
    array, target = case
    assert not function(array, target)
