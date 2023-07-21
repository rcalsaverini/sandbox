from dataclasses import dataclass
from functools import wraps
from typing import Callable, Generic, List, TypeVar

F = TypeVar("F")
A = TypeVar("A")
B = TypeVar("B")

class Subscript(Generic[F, A]):
    pass

class Typeclass:
    __instances__ = {}
    
    def __init__(self, *typevars):
        print(typevars)
    
    def __call__(self, klass):
        
        def typeclass_instanciation(*typevars):
            def wrap_klass(klass):
                @wraps(klass)
                def wrapped_klass(*args, **kwargs):
                    return klass(*args, **kwargs)
                return wrapped_klass
            return wrap_klass
        
        def method_instanciation(*typevars):
            def wrap_method(method):
                @wraps(method)
                def wrapped_method(*args, **kwargs):
                    return method(*args, **kwargs)
                return wrapped_method
            return wrap_method
        
        klass.instance = typeclass_instanciation
        klass.method = method_instanciation
        return klass
    
    @classmethod
    def method(cls, *typevars):
        print(typevars)
        def wrap_method(method):
            @wraps(method)
            def wrapped_method(*args, **kwargs):
                return method(*args, **kwargs)
            return wrapped_method
        return wrap_method
    
    @classmethod
    def instance(cls, klass):
        print(klass)
        return klass
    
@Typeclass(F)
class Functor:

    @Typeclass.method(A, B)
    def fmap(item: Subscript[F, A], function: Callable[[A], B]) -> Subscript[F, B]:
        raise NotImplementedError


@Functor.instance(List)
class FunctorList:
    
    @Functor.method(A, B)
    def fmap(xs: List[A], function: Callable[[A], B]) -> List[B]:
        return [function(x) for x in xs]