from pytest import fixture
from src.event import Event, EventType
from src.expr import Attr, Literal


@fixture
def event():
    return Event(
        event_type=EventType.CC_TRANSACTION,
        attributes={
            "test": "this is a test",
            "age": 42,
            "is_active": True,
            "is_inactive": False,
        },
        timestamp=0,
    )


def test_eq(event):
    x = Attr("age")
    y = Literal(42)
    assert (x == y).eval(event)


def test_ne(event):
    x = Attr("age")
    y = Literal(42)
    assert not (x != y).eval(event)


def test_gt(event):
    x = Attr("age")
    y = Literal(41)
    assert (x > y).eval(event)


def test_lt(event):
    x = Attr("age")
    y = Literal(43)
    assert (x < y).eval(event)


def test_ge(event):
    x = Attr("age")
    y = Literal(42)
    assert (x >= y).eval(event)


def test_le(event):
    x = Attr("age")
    y = Literal(42)
    assert (x <= y).eval(event)


def test_and(event):
    t1 = Literal(True)
    t2 = Literal(True)
    f1 = Literal(False)
    f2 = Literal(False)

    assert (t1 & t2).eval(event)
    assert not (t1 & f1).eval(event)
    assert not (f1 & t1).eval(event)
    assert not (f1 & f2).eval(event)


def test_or(event):
    t1 = Literal(True)
    t2 = Literal(True)
    f1 = Literal(False)
    f2 = Literal(False)

    assert (t1 | t2).eval(event)
    assert (t1 | f1).eval(event)
    assert (f1 | t1).eval(event)
    assert not (f1 | f2).eval(event)


def test_not(event):
    t = Literal(True)
    f = Literal(False)

    assert not (~t).eval(event)
    assert (~f).eval(event)


def test_add(event):
    x = Attr("age")
    y = Literal(1)
    assert (x + y).eval(event) == 43


def test_sub(event):
    x = Attr("age")
    y = Literal(1)
    assert (x - y).eval(event) == 41


def test_mul(event):
    x = Attr("age")
    y = Literal(2)
    assert (x * y).eval(event) == 84


def test_truediv(event):
    x = Attr("age")
    y = Literal(2)
    assert (x / y).eval(event) == 21


def test_pow(event):
    x = Attr("age")
    assert (x**2).eval(event) == 1764


def test_neg(event):
    x = Attr("age")
    assert (-x).eval(event) == -42


def test_pos(event):
    x = Attr("age")
    assert (+x).eval(event) == 42


def test_abs(event):
    x = Literal(-42)
    assert abs(x).eval(event) == 42
