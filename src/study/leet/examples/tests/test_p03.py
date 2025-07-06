import pytest
from hypothesis import given, strategies as st
from examples.p03 import solution_brute_force

functions = [solution_brute_force]


@st.composite
def create_case(draw) -> tuple[list[int], list[int]]:
    st_values = st.integers(min_value=0, max_value=100)
    st_repeats = st.integers(min_value=2, max_value=3)
    repetitions_spec = draw(
        st.dictionaries(st_values, st_repeats, min_size=2, max_size=5)
    )
    repetitions = [k for k, v in repetitions_spec.items() for _ in range(v)]
    arr = draw(st.permutations(repetitions))
    repeating_numbers = {k for k, v in repetitions_spec.items() if v > 1}
    return arr, repeating_numbers


@given(create_case())
@pytest.mark.parametrize("function", functions)
def test_cases(function, case):
    arr, repeating_numbers = case
    assert function(arr) == repeating_numbers
