from multiprocessing.sharedctypes import Value
from typing import TypeVar
import numpy as np
from numpy.typing import ArrayLike


def get_sequence_size(sequence):
    (n, *_) = sequence.shape
    if len(_) != 0:
        raise ValueError("Input must be a 1D array")
    return n


def generate_wall(sequence, depth=10):
    n = get_sequence_size(sequence)
    wall = np.zeros((depth, n + 2))
    wall[0, :] = np.ones(n + 2)
    wall[1, 1:-1] = sequence
    for k in range(1, n - 2):
        wall[k + 1, 1:-1] = (wall[k, 1:-1] ** 2 - wall[k, 2:] * wall[k, 0:-2]) / wall[
            k - 1, 1:-1
        ]
    return wall
