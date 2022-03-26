from functools import singledispatch, update_wrapper
import methods
import numpy as np

def methdispatch(func):
    dispatcher = singledispatch(func)
    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper

class Array(object):
    # INIT
    @methdispatch
    def __init__(self, array):
        self.values = array()
    @__init__.register(list)
    def _(self, array):
        self.values = np.longcomplex(array)
    @__init__.register(np.ndarray)
    def _(self, array):
        self.values = array.copy()

    # MISC
    def __call__(self) -> np.ndarray:
        return self.values.copy()
    def __str__(self):
        return str(self.values.copy())
    def __getitem__(self, key):
        return self.values[key]

    # +
    # Arrays
    @methdispatch
    def __add__(self, other)  :
        new_Array = Array(self.values)
        new_Array += other()
        return new_Array
    @__add__.register
    def _(self, other:list)  :
        other = Array(other)
        return self.__add__(other)
    @__add__.register
    def _(self, other:np.ndarray)  :
        other = Array(other)
        return self.__add__(other)
    # Numbers
    @__add__.register
    def _(self, other:np.longcomplex)  :
        new_Array = Array(self.values)
        new_Array += other
        return new_Array
    @__add__.register
    def _(self, other:float)  :
        other = np.longcomplex(other)
        return self.__add__(other)

    # +=
    # Arrays
    @methdispatch
    def __iadd__(self, other):
        self.values += other()
        return self
    @__iadd__.register
    def _(self, other:list)  :
        other = Array(other)
        return self.__iadd__(other)
    @__iadd__.register
    def _(self, other:np.ndarray)  :
        other = Array(other)
        return self.__iadd__(other)
    @__iadd__.register
    # Numbers
    def _(self, other:np.longcomplex)  :
        self.values += other
        return self
    @__iadd__.register
    def _(self, other:float)  :
        other = np.longcomplex(other)
        return self.__iadd__(other)

    # *
    # Arrays
    @methdispatch
    def __mul__(self, other):
        new_Array = Array(self.values)
        new_Array *= other()
        return new_Array
    @__mul__.register
    def _(self, other:list) :
        other = Array(other)
        return self.__mul__(other)
    @__add__.register
    def _(self, other:np.ndarray):
        other = Array(other)
        return self.__mul__(other)
    # Numbers
    @__add__.register
    def _(self, other:np.longcomplex):
        new_Array = Array(self.values)
        new_Array *= other
        return new_Array
    @__add__.register
    def _(self, other:float):
        other = np.longcomplex(other)
        return self.__mul__(other)

    # *=
    # Arrays
    @methdispatch
    def __imul__(self, other):
        self.values = np.multiply(self.values, other.values)
        return self
    @__imul__.register
    def _(self, other:list) :
        other = Array(other)
        return self.__imul__(other)
    @__imul__.register
    def _(self, other:np.ndarray):
        other = Array(other)
        return self.__imul__(other)
    # Numbers
    @__imul__.register
    def _(self, other:np.longcomplex):
        self.values *= other
        return self
    @__imul__.register
    def _(self, other:float):
        self.values *= np.longcomplex(other)
        return self

class Solver(object):
    def __init__(array:"Array") -> "Array":
        self.array = Array(array)
        if self.array[3]!=lc(1):
	        item = self.array[3].copy()
	        self.array = lc(list(map(lambda x: x/item, self.array())))
        self.array = Array(array)
    
    def solve(self):
        Q = (inp[2]**lc(2) - 3*inp[1])/9
        R = (2*inp[2]**3-9*inp[1]*inp[2]+27*inp[0])/54
        S = Q**3 - R**2
