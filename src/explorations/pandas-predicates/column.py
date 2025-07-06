from typing import Any
from pandera.typing import DataFrame, Series, Bool
from .predicate import Predicate
from .strings import Str
from .dates import Date


class col:
    
    def __init__(self, name: str):
        self.name = name
    
    def __eq__(self, value: Any) -> Predicate:
        return Eq(self.name, value)
    
    def __ne__(self, value: Any) -> Predicate:
        return Ne(self.name, value)
    
    def __gt__(self, value: Any) -> Predicate:
        return Gt(self.name, value)
    
    def __ge__(self, value: Any) -> Predicate:
        return Ge(self.name, value)
    
    def __lt__(self, value: Any) -> Predicate:
        return Lt(self.name, value)
    
    def __le__(self, value: Any) -> Predicate:
        return Le(self.name, value)
    
    def isin(self, values: list) -> Predicate:
        raise NotImplementedError("Not implemented yet")
    
    def between(self, lower: Any, upper: Any) -> Predicate:
        raise NotImplementedError("Not implemented yet")
    
    def isna(self) -> Predicate:
        raise NotImplementedError("Not implemented yet")
    
    def isnull(self) -> Predicate:
        raise NotImplementedError("Not implemented yet")
    
    @property
    def str(self) -> Str:
        return Str(self.name)
    
    @property
    def dt(self) -> Date:
        return Date(self.name)


class Eq(Predicate):
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value
        
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        return dataframe[self.name] == self.value
    

class Ne(Predicate):
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value
        
    def mask(self, dataframe: DataFrame) -> DataFrame:
        return dataframe[self.name] != self.value

class Gt(Predicate):
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value
        
    def mask(self, dataframe: DataFrame) -> DataFrame:
        return dataframe[self.name] > self.value
    
class Ge(Predicate):
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value
        
    def mask(self, dataframe: DataFrame) -> DataFrame:
        return dataframe[self.name] >= self.value
    
class Lt(Predicate):
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value
        
    def mask(self, dataframe: DataFrame) -> DataFrame:
        return dataframe[self.name] < self.value
    
class Le(Predicate):
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value
        
    def mask(self, dataframe: DataFrame) -> DataFrame:
        return dataframe[self.name] <= self.value

