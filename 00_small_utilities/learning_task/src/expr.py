from typing import Generic, TypeVar, Optional
from dataclasses import dataclass
from src.event import Event

A = TypeVar("A")


class Expr(Generic[A]):
    def eval(self, event: Event) -> A:
        raise NotImplementedError("eval")

    # Comparison operators

    def __eq__(self, other: "Expr[A]") -> "Expr[bool]":
        return Equal(self, other)

    def __ne__(self, other: "Expr[A]") -> "Expr[bool]":
        return Not(Equal(self, other))

    def __gt__(self, other: "Expr[A]") -> "Expr[bool]":
        return GreaterThan(self, other)

    def __lt__(self, other: "Expr[A]") -> "Expr[bool]":
        return LessThan(self, other)

    def __ge__(self, other: "Expr[A]") -> "Expr[bool]":
        return Not(LessThan(self, other))

    def __le__(self, other: "Expr[A]") -> "Expr[bool]":
        return Not(GreaterThan(self, other))

    # Logical operators

    def __and__(self, other: "Expr[bool]") -> "Expr[bool]":
        return And(self, other)

    def __or__(self, other: "Expr[bool]") -> "Expr[bool]":
        return Or(self, other)

    def __invert__(self) -> "Expr[bool]":
        return Not(self)

    # Arithmetic operators

    def __add__(self, other: "Expr[A]") -> "Expr[A]":
        return Add(self, other)

    def __sub__(self, other: "Expr[A]") -> "Expr[A]":
        return Sub(self, other)

    def __mul__(self, other: "Expr[A]") -> "Expr[A]":
        return Mul(self, other)

    def __truediv__(self, other: "Expr[A]") -> "Expr[A]":
        return Div(self, other)

    def __pow__(self, exponent: int) -> "Expr[A]":
        return Pow(self, exponent)

    def __neg__(self) -> "Expr[A]":
        return Neg(self)

    def __pos__(self) -> "Expr[A]":
        return Pos(self)

    def __abs__(self) -> "Expr[A]":
        return Abs(self)

    def __call__(self, event: Event) -> A:
        return self.eval(event)


class Attr(Expr[A]):
    def __init__(self, name: str):
        self.name = name

    def eval(self, event: Event) -> A:
        return event.attributes[self.name]

    def __str__(self):
        return "Attr(f{self.name})"


class Literal(Expr[A]):
    def __init__(self, value: A):
        self.value = value

    def eval(self, event: Event) -> A:
        return self.value

    def __str__(self):
        return f"Literal({self.value})"


@dataclass
class Equal(Expr[bool]):
    left: A
    right: A

    def eval(self, event: Event) -> Optional[bool]:
        return self.left.eval(event) == self.right.eval(event)

    def __str__(self):
        return f"({self.left} == {self.right})"


@dataclass
class GreaterThan(Expr[bool]):
    left: A
    right: A

    def eval(self, event: Event) -> Optional[bool]:
        return self.left.eval(event) > self.right.eval(event)

    def __str__(self):
        return f"({self.left} > {self.right})"


@dataclass
class LessThan(Expr[bool]):
    left: A
    right: A

    def eval(self, event: Event) -> Optional[bool]:
        return self.left.eval(event) < self.right.eval(event)


class Not(Expr[bool]):
    def __init__(self, expr: Expr[bool]):
        self.expr = expr

    def eval(self, event: Event) -> bool:
        return not self.expr.eval(event)

    def __str__(self):
        return f"not {self.expr}"


class Or(Expr[bool]):
    def __init__(self, left: Expr[bool], right: Expr[bool]):
        self.left = left
        self.right = right

    def eval(self, event: Event) -> bool:
        return self.left.eval(event) or self.right.eval(event)

    def __str__(self):
        return f"({self.left} | {self.right})"


class And(Expr[bool]):
    def __init__(self, left: Expr[bool], right: Expr[bool]):
        self.left = left
        self.right = right

    def eval(self, event: Event) -> bool:
        return self.left.eval(event) and self.right.eval(event)


class Add(Expr[A]):
    def __init__(self, left: Expr[A], right: Expr[A]):
        self.left = left
        self.right = right

    def eval(self, event: Event) -> A:
        return self.left.eval(event) + self.right.eval(event)

    def __str__(self):
        return f"({self.left} + {self.right})"


class Sub(Expr[A]):
    def __init__(self, left: Expr[A], right: Expr[A]):
        self.left = left
        self.right = right

    def eval(self, event: Event) -> A:
        return self.left.eval(event) - self.right.eval(event)

    def __str__(self):
        return f"({self.left} - {self.right})"


class Mul(Expr[A]):
    def __init__(self, left: Expr[A], right: Expr[A]):
        self.left = left
        self.right = right

    def eval(self, event: Event) -> A:
        return self.left.eval(event) * self.right.eval(event)

    def __str__(self):
        return f"({self.left} * {self.right})"


class Div(Expr[A]):
    def __init__(self, left: Expr[A], right: Expr[A]):
        self.left = left
        self.right = right

    def eval(self, event: Event) -> A:
        return self.left.eval(event) / self.right.eval(event)

    def __str__(self):
        return f"({self.left} / {self.right})"


class Pow(Expr[A]):
    def __init__(self, expr: Expr[A], exponent: int):
        self.expr = expr
        self.exponent = exponent

    def eval(self, event: Event) -> A:
        return self.expr.eval(event) ** self.exponent

    def __str__(self):
        return f"({self.expr} ** {self.exponent})"


class Neg(Expr[A]):
    def __init__(self, expr: Expr[A]):
        self.expr = expr

    def eval(self, event: Event) -> A:
        return -self.expr.eval(event)

    def __str__(self):
        return f"(-{self.expr})"


class Pos(Expr[A]):
    def __init__(self, expr: Expr[A]):
        self.expr = expr

    def eval(self, event: Event) -> A:
        return +self.expr.eval(event)


class Abs(Expr[A]):
    def __init__(self, expr: Expr[A]):
        self.expr = expr

    def eval(self, event: Event) -> A:
        return abs(self.expr.eval(event))

    def __str__(self):
        return f"abs({self.expr})"
