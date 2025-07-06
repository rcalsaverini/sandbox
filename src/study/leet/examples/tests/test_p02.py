import pytest
from hypothesis import given, strategies as st
from examples.p02 import solution_brute_force, solution_single_pass

functions = [solution_brute_force, solution_single_pass]


@st.composite
def create_case(draw) -> tuple[list[int], int]:
    max_profit = draw(st.integers(min_value=5, max_value=100))
    seq_profits = draw(
        st.lists(
            st.integers(min_value=0, max_value=max_profit), min_size=2, max_size=10
        )
    )
    i = draw(st.integers(min_value=0, max_value=len(seq_profits) - 1))
    seq_profits[i] = max_profit
    first_price = draw(st.integers(min_value=0, max_value=100))
    arr = [first_price]
    for profit in seq_profits:
        current_min_price = min(arr)
        arr.append(current_min_price + profit)
    return (arr, max_profit)


@given(create_case())
@pytest.mark.parametrize("function", functions)
def test_cases(function, case):
    prices, day = case
    assert function(prices) == day
