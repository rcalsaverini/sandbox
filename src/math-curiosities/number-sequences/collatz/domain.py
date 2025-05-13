from nptyping import NDArray, Int, Shape
from typing import Callable

Orbit = NDArray[Shape["N"], Int]
Rule = Callable[[int], int]
IteratedRule = Callable[[int], Orbit]
