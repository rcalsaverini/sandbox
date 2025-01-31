from typing import ClassVar, TypeVar, Generic
from dataclasses import dataclass


class PenguinMeta(type):
    def __new__(mcs, name, bases, namespace):
        out = super().__new__(mcs, name, bases, namespace)
        out.annotations = namespace.get("__annotations__", {})
        return out


A = TypeVar("A", bound="UserF")


class UserF(Generic[A], metaclass=PenguinMeta):
    name: str
    friends: list[A]
