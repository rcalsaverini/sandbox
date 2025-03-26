from typing import TypeVar, Generic
from timeit import default_timer as timer
from random import randint
from tqdm import trange

A = TypeVar("A")
K = TypeVar("K")


class AccessTable(Generic[A]):
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def insert(self, key: int, value: A):
        self.table[key] = value

    def get(self, key: int) -> A | None:
        return self.table[key]

    def delete(self, key: int):
        self.table[key] = None


class HashTable(Generic[K, A]):
    def __init__(self, size):
        self.size = size
        self.table = AccessTable(size)

    def insert(self, key: K, value: A):
        self.table.insert(hash(key) % self.size, value)

    def get(self, key: int) -> A | None:
        return self.table.get(hash(key) % self.size)

    def delete(self, key: int):
        self.table.delete(hash(key) % self.size)


def random_string(length):
    return "".join([chr(randint(65, 122)) for i in range(length)])


def time_insert(size, num_trials):
    ht = HashTable[str, int](size)
    start = timer()
    for i in range(num_trials):
        key = random_string(5)
        ht.insert(key, i)
    end = timer()
    return end - start


def main():
    with open("data/hashtable.csv", "w") as f:
        print("trials,size,time", file=f)
        for size in trange(100_000, 1_000_000, 10_000):
            for num_trials in trange(1_000, 10_000, 100):
                print(f"{num_trials}, {size}, {time_insert(size, num_trials)}", file=f)


if __name__ == "__main__":
    main()
