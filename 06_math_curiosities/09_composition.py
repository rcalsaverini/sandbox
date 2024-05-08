from dataclasses import dataclass
from functools import reduce
from typing import Callable, TypeVar, Generic
import numpy as np
import matplotlib.pyplot as plt

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

@dataclass
class bijection(Generic[A, B]):
    forward: Callable[[A], B]
    backward: Callable[[B], A]
    
    def __call__(self, a: A) -> B:
        return self.forward(a)
    
    @property
    def inverse(self) -> 'bijection[B, A]':
        return bijection(self.backward, self.forward)
    
    def __mul__(self, other: 'bijection[B, C]') -> 'bijection[A, C]':
        return bijection(lambda a: other(self(a)), lambda c: self.inverse(other.inverse(c)))
    

def compose(*bijections: bijection) -> bijection:
    return bijection(lambda a: reduce(lambda x, f: f(x), bijections, a), lambda c: reduce(lambda x, f: f(x), reversed(bijections), c))

@dataclass
class number:
    
    value: float
    mapping: bijection[float, float]
    adder: Callable[[float, float], float]
    
    def __add__(self, other: 'number') -> 'number':
        return self.mapping.inverse(self.adder(self.mapping(self.value), other.mapping(other.value)))    

identity = bijection(lambda x: x, lambda x: x)
exponential = bijection(lambda x: np.exp(x), lambda x: np.log(x))
power = lambda n: bijection(lambda x: x**n, lambda x: x**(1/n))
logarithm = exponential.inverse
roots = lambda n: power(1.0/n)

exponential_numbers = lambda value: number(value, exponential, lambda x, y: x * y)
trigonometric_numbers = lambda value: number(value, bijection(np.sin, np.arcsin), lambda x, y: x + y)

def plot_spheres():
    xs = np.linspace(-1, 1, 100)
    ys = np.linspace(-1, 1, 100)
    x_grid, y_grid = np.meshgrid(xs, ys)
    z_grid = exponential_numbers(x_grid) + exponential_numbers(y_grid)
    z_values = np.percentile(z_grid.flatten(), [0, 25, 50, 75, 100])
    
    for z in z_values:
        plt.contourf(x_grid, y_grid, z_grid, levels=[-np.inf, z], colors='k')
        
        
plot_spheres()
plt.show()


