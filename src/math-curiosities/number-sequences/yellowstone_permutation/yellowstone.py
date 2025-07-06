from dataclasses import dataclass
from typing import Callable, Generic, Iterable, TypeVar, Self, List
from itertools import chain

T = TypeVar("T")
A = TypeVar("A")
Equivalence = Callable[[T, T], bool]
SortKey = Callable[[T], float]


class YellowstoneBuilder(Generic[A]):  
    def with_items(self, items: Iterable[A]) -> Self:
        self.items = items
        return self
    
    def with_equivalence(self, equivalence: Equivalence[A]) -> Self:
        self.equivalence = equivalence
        return self
    
    def with_sort_key(self, sort_key: SortKey[A]) -> Self:
        self.sort_key = sort_key
        return self
    
    def ready(self) -> Yellowstone[A]:
        return Yellowstone(self.items, self.equivalence, self.sort_key)
    

@dataclass
class Yellowstone(Generic[A]):
    items: Iterable[A]
    equivalence: Equivalence[A]
    sort_key: SortKey[A]
    
    @staticmethod
    @property
    def build() -> YellowstoneBuilder[A]:
        return YellowstoneBuilder()
    
    
    def filter(self, items: List[A], prototype: A, anti_prototype: A):
        return [
            item 
            for item in items 
            if self.equivalence(item, prototype) 
            and not self.equivalence(item, anti_prototype)
        ]
    
        
    def _step_on_reservoir(self, reservoir: List[A], prototype: A, anti_prototype: A) -> Iterable[A]:
        is_valid = lambda x: self.equivalence(x, prototype) and not self.equivalence(x, anti_prototype)        
        reservoir_candidates = filter(is_valid, reservoir)
        try:
            output = next(reservoir_candidates)
            new_reservoir = [x for x in reservoir if x != output]
            return output, new_reservoir
        except StopIteration:
            return None, reservoir

    def _step_outside_of_reservoir(self, prototype: A, anti_prototype: A) -> Iterable[A]:
        reservoir = []
        is_valid = lambda x: self.equivalence(x, prototype) and not self.equivalence(x, anti_prototype)
        for item in self.items:
            if is_valid(item):
                break
            else:
                reservoir.append(item)
        return item, reservoir
    
    def step(self, reservoir: List[A], prototype: A, anti_prototype: A) -> Iterable[A]:
        output, reservoir = self._step_on_reservoir(reservoir, prototype, anti_prototype)
        if output is None:
            output, new_reservoir = self._step_outside_of_reservoir(prototype, anti_prototype)
            reservoir += new_reservoir
        return output, reservoir
    
    def __iter__(self) -> Iterable[A]:
        last = next(self.items)
        current = next(self.items)
        reservoir = []
        while True:
            is_valid = lambda x: self.equivalence(x, last) and not self.equivalence(x, current)
            candidate = None
            for candidate in chain(reservoir, self.items):
                if not is_valid(candidate):
                    reservoir.append(candidate)
                else:
                    reservoir.remove(candidate)
                    break
            if candidate is None:
                break
            else:
                yield candidate