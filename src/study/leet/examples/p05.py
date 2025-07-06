"""
Exercises involving stacks
"""

OPERATORS = ["+", "-", "*", "/"]
OPERANDS = [chr(i) for i in range(97, 123)]


def infix_to_postfix(expression: str) -> str:
    def consume_operand(expression: str) -> tuple[str, str]:
        """
        Consume an operand from the expression
        """
        stack = [expression[0]]
        expression = expression[1:]
        operand = ""
        while len(stack) > 0:
            if len(expression) == 0:
                break
            if expression[0] == ")":
                stack.pop()
            elif expression[0] == "(":
                stack.append("(")
            else:
                operand += expression[0]
            expression = expression[1:]
        return operand, expression

    if not expression:
        return ""

    if expression[0] == "(":
        left_operand, expression = consume_operand(expression)
        operator = expression[0]
        right_operand, expression = consume_operand(expression[1:])
        return f"{infix_to_postfix(left_operand)}{infix_to_postfix(right_operand)}{operator}"
