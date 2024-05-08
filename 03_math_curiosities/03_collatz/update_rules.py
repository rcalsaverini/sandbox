from typing import Dict, List
from domain import Rule
from sympy import factorint, isprime
from random import choice

def collatz(x: int) -> int:
    return x // 2 if x % 2 == 0 else 3 * x + 1

def collatz_23(x: int) -> int:
    if x % 2 == 0:
        return x // 2
    elif x % 3 == 0:
        return x // 3
    return (x * x - 1) // 24

def make_collatz_prime_rule(prime: int) -> Rule:
    def collatz_prime(x: int) -> int:
        if x % prime == 0:
            return x // prime
        return collatz(x)
    return collatz_prime
    

def make_collatz_primes_rule(primes: List[int]) -> Rule:
    def collatz_primes(x: int) -> int:
        for prime in primes:
            if x % prime == 0:
                return x // prime
        return collatz(x)
    return collatz_primes


def prime_stairs(x: int) -> int:
    if x == 1: 
        return 1

    factors: Dict[int, int] = factorint(x)
    max_factor = max(factors)
    is_prime = max_factor == x
    return  (x * x - 1) if is_prime else (x // max_factor)


def prime_collatz(x: int) -> int:
    if isprime(x):
        return 3 * x + 1
    elif x == 1:
        return 1
    else:
        min_factors = min(factorint(x))
        return x // min_factors
    
def random_binance(x: int) -> int:
    if x == 0:
        return x
    if x == 1:
        return 1
    random_factor = choice(list(factorint(x).keys()))
    try:
        return 3 * (x // random_factor) + 1
    except:
        print(x, random_factor)
        raise
    

# inverted creating of the prime stairs rule
# def maps_to_prime(node):
#     factors = factorint(node + 1) 
#     has_only_one_factor = len(factors) == 1
#     power_is_two = list(factors.values())[0] == 2
#     return has_only_one_factor and power_is_two

# def reverse_prime_stairs(node, max_prime=10):
#     return list(sorted(
#         prime_multiples(node, max_prime) + 
#         anti_stair(node)
#     ))
    
# def prime_multiples(node, max_prime):
#     factors = factorint(node)
#     max_factor = max(factors)
#     return [p * node for p in primerange(max_factor, max_prime)]

# def anti_stair(node):
#     factors = factorint(node + 1)
#     if len(factors) == 1:
#         (p, n), *_ = factorint(node + 1).items()
#         return [p] if n == 2 else []
#     else:
#         return []
