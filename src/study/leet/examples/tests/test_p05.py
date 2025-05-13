"""
Test cases for p05.py
Exercises involving stacks
"""

import pytest
from hypothesis import given, strategies as st
from examples.p05 import infix_to_postfix, OPERATORS, OPERANDS


def to_infix(tree: tuple[str, str, str]) -> str:
    if len(tree) == 1:
        return tree[0]
    return f"({to_infix(tree[0])}{tree[1]}{to_infix(tree[2])})"


def to_postfix(tree: tuple[str, str, str]) -> str:
    if len(tree) == 1:
        return tree[0]
    return f"{to_postfix(tree[0])}{to_postfix(tree[2])}{tree[1]}"


@st.composite
def st_expressions(draw) -> tuple[str, str]:
    """
    Generate a pair of infix and postfix expressions
    Ex.: ('a+b', 'ab+')
    """

    expression_tree = draw(
        st.recursive(
            st.sampled_from(OPERANDS),
            lambda children: st.tuples(children, st.sampled_from(OPERATORS), children),
        )
    )

    return to_infix(expression_tree), to_postfix(expression_tree)


@given(st_expressions())
def test_infix_to_postfix(expressions):
    expression_infix, expression_postfix = expressions
    assert infix_to_postfix(expression_infix) == expression_postfix
