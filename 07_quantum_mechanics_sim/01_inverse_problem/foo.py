from abc import abstractmethod
from typing import Callable, Generic, TypeVar
from dataclasses import dataclass

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class Maybe(Generic[A]):
    @staticmethod
    def makeValue(value: A) -> "Maybe[A]":
        return Value(value)

    @staticmethod
    def makeError(error: Exception) -> "Maybe[A]":
        return Error(error)

    @classmethod
    def apply(cls, f: Callable[[B], A], *args, **kwargs) -> "Maybe[A]":
        try:
            return cls.makeValue(f(*args, **kwargs))
        except Exception as e:
            return cls.makeError(e)

    @abstractmethod
    def map(self, f: Callable[[A], B]) -> "Maybe[B]":
        raise NotImplementedError()

    @abstractmethod
    def flatmap(self, f: Callable[[A], "Maybe[B]"]) -> "Maybe[B]":
        raise NotImplementedError()

    @abstractmethod
    def getOrRaise(self) -> A:
        raise NotImplementedError()
    
    def __


@dataclass
class Value(Maybe[A]):
    value: A

    def getOrRaise(self) -> A:
        return self.value

    def map(self, f: Callable[[A], B]) -> "Maybe[B]":
        return Value(f(self.value))

    def flatmap(self, f: Callable[[A], "Maybe[B]"]) -> "Maybe[B]":
        return f(self.value)


@dataclass
class Error(Maybe[A]):
    error: Exception

    def getOrRaise(self) -> A:
        raise self.error

    def map(self, f: Callable[[A], B]) -> "Maybe[B]":
        return Error(self.error)

    def flatmap(self, f: Callable[[A], "Maybe[B]"]) -> "Maybe[B]":
        return Error(self.error)


x: Maybe[int] = Value(1)

x.map(lambda x: x - 1).map(lambda x: 1 / x).getOrRaise()
