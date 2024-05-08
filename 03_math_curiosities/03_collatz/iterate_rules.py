from domain import Rule, IteratedRule, Orbit, Callable
import numpy as np


def iterate_rule(update_rule: Rule, max_iterations: int = 0) -> IteratedRule:
    def iterated_rule(start: int) -> Orbit:
        x = start
        output = [x]
        for _ in range(max_iterations):
            x = update_rule(x)
            output.append(x)
        return np.array(output).astype(int)
    return iterated_rule


def iterate_until(update_rule: Rule) -> Callable[[int, int], Orbit]:
    def iterate_until(start: int, target: int) -> Orbit:
        x = start
        output = [x]
        while x != target:
            x = update_rule(x)
            output.append(x)
        return np.array(output).astype(int)
    return iterate_until


def reaches_target(update_rule: Rule, max_iterations: int = 0) -> Callable[[int, int], bool]:
    iterated_rule = iterate_rule(update_rule, max_iterations)
    
    def reaches_target(start: int, target: int) -> bool:
        x = start
        orbit = iterated_rule(start)
        return target in set(orbit.tolist())
        
    return reaches_target
    
