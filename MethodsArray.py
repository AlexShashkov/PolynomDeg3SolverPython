from functools import singledispatch, update_wrapper
from types import SimpleNamespace
import numpy as np
from numpy import longcomplex as lc

def methdispatch(func):
    dispatcher = singledispatch(func)
    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


class Struct(SimpleNamespace):
    # Для хранения степеней числа
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def __call__(self):
        return self.init
    def expand(self, **kwargs):
        for key, value in kwargs.items():
            #print(key, value)
            #vars()[key] = value
            setattr(self, key, value)

class Array(object):
    # INIT
    @methdispatch
    def __init__(self, array):
        self.outputf = None
        self.values = array()
        if self.values.ndim == 1:
            self.values = self.values.reshape((1, self.values.shape[0]))
        self.shape = self.values.shape
    @__init__.register(list)
    def _(self, array):
        self.outputf = None
        self.values = np.longcomplex(array)
        if self.values.ndim == 1:
           self.values = self.values.reshape((1, self.values.shape[0]))
        self.shape = self.values.shape
    @__init__.register(np.ndarray)
    def _(self, array):
        self.outputf = None
        self.values = array.copy()
        if self.values.ndim == 1:
            self.values = self.values.reshape((1, self.values.shape[0]))
        self.shape = self.values.shape

    # MISC
    def setOutputFunction(self, func):
        self.outputf = func
    def __call__(self) -> np.ndarray:
        return self.values.copy()
    def __str__(self):
        if self.outputf is not None:
            return self.outputf(self)
        else:
            return f"Vieta array:{self.shape}:\n{str(self.values.copy())}"
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
    @__add__.register
    def _(self, other:int):
        other = np.longcomplex(other)
        return self.__mul__(other)
    @__add__.register
    def _(self, other:complex):
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
    @__imul__.register
    def _(self, other:int):
        self.values *= np.longcomplex(other)
        return self
    @__imul__.register
    def _(self, other:complex):
        self.values *= np.longcomplex(other)
        return self

