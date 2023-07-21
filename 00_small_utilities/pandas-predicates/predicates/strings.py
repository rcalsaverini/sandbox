from .predicate import Predicate
from pandera.typing import DataFrame, Series, Bool
import re

class Str:
    
    def __init__(self, name: str):
        self.name = name
        
    def contains(self, pat: str, case=True, flags=0, na=None, regex=True) -> Predicate:
        return Contains(self.name, pat, case=case, flags=flags, na=na, regex=regex)

    def fullmatch(self, pat: str, case=True, flags=0, na=None) -> Predicate:
        return FullMatch(self.name, pat, case=case, flags=flags, na=na)
    
    def match(self, pat: str, case=True, flags=0, na=None) -> Predicate:
        return Match(self.name, pat, case=case, flags=flags, na=na)
    
    def startswith(self, pat: str, na=None) -> Predicate:
        return StartsWith(self.name, pat, na=na)
    
    def isalnum(self) -> Predicate:
        return IsAlNum(self.name)
    
    def isalpha(self) -> Predicate:
        raise NotImplementedError("Not implemented yet.")

    def isdigit(self) -> Predicate:
        raise NotImplementedError("Not implemented yet.")

    def isspace(self) -> Predicate:
        raise NotImplementedError("Not implemented yet.")

    def islower(self) -> Predicate:
        raise NotImplementedError("Not implemented yet.")

    def isupper(self) -> Predicate:
        raise NotImplementedError("Not implemented yet.")

    def istitle(self) -> Predicate:
        raise NotImplementedError("Not implemented yet.")

    def isnumeric(self) -> Predicate:
        raise NotImplementedError("Not implemented yet.")

    def isdecimal(self) -> Predicate:
        raise NotImplementedError("Not implemented yet.")

class Contains(Predicate):
    def __init__(self, name: str, pat: str, case=True, flags=0, na=None, regex=True):
        self.name = name
        if regex:
            self.pat = re.compile(pat, flags=flags)
        else:
            self.pat = pat
        self.case = case
        self.flags = flags
        self.na = na
        self.regex = regex
        
        
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        return dataframe[self.name].str.contains(
            self.pat,
            case=self.case,
            flags=self.flags,
            na=self.na,
            regex=self.regex
        )
        
class FullMatch(Predicate):
    def __init__(self, name: str, pat: str, case=True, flags=0, na=None):
        self.name = name
        self.pat = re.compile(pat, flags=flags)
        self.case = case
        self.flags = flags
        self.na = na
        
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        return dataframe[self.name].str.fullmatch(
            self.pat,
            case=self.case,
            flags=self.flags,
            na=self.na
        )
        
class Match(Predicate):
    def __init__(self, name: str, pat: str, case=True, flags=0, na=None):
        self.name = name
        self.pat = re.compile(pat, flags=flags)
        self.case = case
        self.flags = flags
        self.na = na
        
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        return dataframe[self.name].str.match(
            self.pat,
            case=self.case,
            flags=self.flags,
            na=self.na
        )
        
class StartsWith(Predicate):
    def __init__(self, name: str, pat: str, na=None):
        self.name = name
        self.pat = pat
        self.na = na
    
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        return dataframe[self.name].str.startswith(
            self.pat,
            na=self.na
        )
        
class IsAlNum(Predicate):
    def __init__(self, name: str):
        self.name = name
        
    def mask(self, dataframe: DataFrame) -> Series[Bool]:
        return dataframe[self.name].str.isalnum()
