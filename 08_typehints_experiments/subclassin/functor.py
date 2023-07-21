from abc import ABC
from typing import List, Callable, TypeVar, Generic

class FunctorInstance(ABC):
    __instances__ = {}
    
    @classmethod
    def add_implementation(cls, type_tag, implementation):
        cls.__instances__[type_tag] = implementation
    
    @classmethod
    def map(cls, function, item):
        match functor_dispatch(item):
            case Map(map=mapper):
                return mapper(function, item)
            case _:
                raise TypeError(f"Cannot map over {item}")

class Map:
    def __init__(self, mapper):
        self.mapper = mapper
        
    @property
    def map(self):
        return self.mapper
    
    
def functor_dispatch(item):
    for _type, mapper in FunctorInstance.__instances__.items():
        if isinstance(item, _type):
            return Map(mapper)
    return None
        
FunctorInstance.add_implementation(List, lambda f, xs: [f(x) for x in xs])    
print(FunctorInstance.__instances__)

class Functor(ABC):
    @classmethod
    def __subclasshook__(cls, C):
        return C in FunctorInstance.__instances__

    def __init__(self, value):
        self.value = value

    def __enter__(self):
        def map_function(function):
            output = FunctorInstance.map(function, self.value)
            self.value = output
            return output

        return map_function
        
    def __exit__(self, *args):
        pass
        
with Functor([1,2,3]) as fmap:
    xs = fmap(lambda x: x + 1)
    ys = fmap(lambda x: x * 2)
    zs = fmap(lambda x: x - sum(ys)/3)

# My objective is to be able to do this:
#   
#   parsed = BeautifulSoup(html)
#   with Monad(parsed, Optional) as m:
#      m.bind(lambda x: x.find('div'))
#      m.bind(lambda x: x.find('p'))
#      m.bind(lambda x: x.find('a'))
#      url = m.fmap(lambda x: x.get('href'))

#   print(url)


# Perhaps even:
#   
#   x: Optional[str] = "123"
#   y: Optional[str] = "456"
#
#   with Monad(x, Optional) as m, Monad(y, Optional) as n:
#      m >> lambda x: re.match(r'\d+', x)
#      n >> lambda y: re.match(r'\d+', y)
#      z = (m, n).map(lambda (x, y): x + y)
#   print(z)    # <- this will print None if any of the matches failed and "579" otherwise