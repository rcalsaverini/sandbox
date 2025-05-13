from typing import List
from pandera.typing import DataFrame, Series, Bool
from abc import ABC, abstractmethod

class Predicate(ABC):
    
    def __and__(self, other):
        return And(self, other)
    
    def __or__(self, other):
        return Or(self, other)
    
    def __invert__(self):
        return Not(self)
            
    def filter(self, data: DataFrame) -> DataFrame:
        return data.loc[self.mask(data)]

    @abstractmethod
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        raise NotImplementedError("Abstract method")

def any_of(*matchers: Predicate) -> Predicate:
    return Any(list(matchers))

def all_of(*matchers: Predicate) -> Predicate:
    return All(list(matchers))

def none_of(*matchers: Predicate) -> Predicate:
    return Not(any_of(*matchers))

def never() -> Predicate:
    return Never()

def always() -> Predicate:
    return Always()

class And(Predicate):
    def __init__(self, left: Predicate, right: Predicate):
        self.left = left
        self.right = right
        
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        return self.left.mask(dataframe) & self.right.mask(dataframe)
        
class Or(Predicate):
    def __init__(self, left: Predicate, right: Predicate):
        self.left = left
        self.right = right
        
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        return self.left.mask(dataframe) | self.right.mask(dataframe)
    
class Not(Predicate):
    def __init__(self, matcher):
        self.matcher = matcher
    
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        return ~self.matcher.mask(dataframe)
    
class Any(Predicate):
    def __init__(self, matchers: List[Predicate]):
        self.matchers = matchers
        
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        mask = Series([False] * len(dataframe), index=dataframe.index)
        for matcher in self.matchers:
            mask |= matcher.mask(dataframe)
        return mask

class All(Predicate):
    def __init__(self, matchers: List[Predicate]):
        self.matchers = matchers
        
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        mask = Series([True] * len(dataframe), index=dataframe.index)
        for matcher in self.matchers:
            mask &= matcher.mask(dataframe)
        return mask
    
class Never(Predicate):
    
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        return Series([False] * len(dataframe), index=dataframe.index)


class Always(Predicate):
    
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        return Series([True] * len(dataframe), index=dataframe.index)