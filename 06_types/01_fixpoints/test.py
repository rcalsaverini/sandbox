import inspect
from dataclasses import dataclass, make_dataclass
from typing import Any, TypeVar, Generic


def replace_typevar(annotations: dict[str, type], typevar: TypeVar) -> dict[str, type]:
    return {}


def unwire(cls) -> type:
    name = cls.__name__.rstrip("F")
    annotations = inspect.get_annotations(cls)

    @dataclass(frozen=True)
    class Unwired(cls[name]):
        pass

    # typevar = next(v for (k, v) in annotations.items() if isinstance(v, TypeVar))

    Unwired.__qualname__ = name
    Unwired.__name__ = name
    Unwired.__annotations__ = {}

    def unwire(self):
        return Unwired(**{field: getattr(self, field) for field in annotations.keys()})

    return Unwired


def derive_unwired(cls) -> type:
    name = cls.__name__.rstrip("F")
    annotations = inspect.get_annotations(cls)
    new_cls: type = make_dataclass(
        name,
        [(f, t) for f, t in annotations.items()],
        bases=(cls[name],),
        frozen=True,
    )

    globals()[name] = new_cls

    def unwire(self):
        return new_cls(**{field: getattr(self, field) for field in annotations.keys()})

    setattr(cls, "unwire", unwire)

    return cls


# annotations = inspect.get_annotations(cls)
# print(annotations)
# return type(name, (cls,), {})


A = TypeVar("A", bound="UserF")


@derive_unwired
@dataclass(frozen=True)
class UserF(Generic[A]):
    name: str
    friends: list[A]


fooF: UserF[Any] = UserF(name="foo", friends=[])
foo: User = fooF.unwire()


# @dataclass
# class User(UserF["User"]):
#     pass


# @dataclass
# class UserId(UserF["UserId"]):
#     user_id: int


# @dataclass
# class UserJsonFile(UserF["UserJsonFile"]):
#     file: Path

#     @classmethod
#     def from_file(cls, file: Path) -> "UserJsonFile":
#         with open(file, "r") as f:
#             data = json.load(f)
#             friends = [
#                 cls.from_file(friend_path) for friend_path in data["friend_paths"]
#             ]
#             return cls(name=data["name"], friends=friends, file=file)


# def test_fixpoint(user: User) -> User:
#     return user.friends[0]


# def store_db(user: User) -> UserId:
#     new_id = 1  # store in db and get new id
#     friends = [
#         store_db(friend) if isinstance(friend, User) else friend
#         for friend in user.friends
#     ]
#     return UserId(name=user.name, friends=friends, user_id=new_id)
