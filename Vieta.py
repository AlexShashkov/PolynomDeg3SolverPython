from functools import singledispatch, update_wrapper
import methods
import numpy as np
from numpy import longcomplex as lc
import os

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

class Solver(object):
    def __init__(self, array:"Array") -> "Array":
        self.round_dec = bool(os.environ.get('roundto', 1))
        self.array = Array(array)

        if self.array.shape[1] != 4:
            raise Exception("Wrong dimension. Vieta method works only with shapes of (1, 4)!")
    
    def __call__(self) -> Array:
        def _checkA(row):
            newCol = row.copy()
            #print(row)
            if row[3] != 1:
                newCol /= row[3]
            #print(newCol)
            return newCol

        def _Usual(Q, R, S, inp):
            phi = np.arccos(R/np.sqrt(Q**3))/3
            #print("Usual method")
            #print(f"Phi: {phi} ")
            x1 = -2*np.sqrt(Q)*np.cos(phi)-inp[2]/3
            x2 = 2*np.sqrt(Q)*np.cos(phi+2*np.pi/3)-inp[2]/3
            x3 = -2*np.sqrt(Q)*np.cos(phi-2*np.pi/3)-inp[2]/3
            return (x1, x2, x3) 
        def _Complex(Q, R, S, inp):
            #print("Complex method")
            phi = 0
            T = 0
            x2, x3 = 0, 0
            if Q>0:
                phi = methods.arch(np.abs(R)/np.sqrt(np.abs(Q**3)))/3
                T = np.sign(R)*np.sqrt(np.abs(Q))*methods.ch(phi)
                x2 = T - inp[2]/3+1j*np.sqrt(3)*np.sqrt(np.abs(Q))*methods.sh(phi)
                x3 = T - inp[2]/3-1j*np.sqrt(3)*np.sqrt(np.abs(Q))*methods.sh(phi)
            else:
                phi = methods.arsh(np.abs(R)/np.sqrt(np.abs(Q**3)))/3
                T = np.sign(R)*np.sqrt(np.abs(Q))*methods.sh(phi)
                x2 = T - inp[2]/3+1j*np.sqrt(3)*np.sqrt(np.abs(Q))*methods.ch(phi)
                x3 = T - inp[2]/3-1j*np.sqrt(3)*np.sqrt(np.abs(Q))*methods.ch(phi)
            #print(f"Phi: {phi}, T: {T}")
            x1 = -2*T-inp[2]/3
            return (x1, x2, x3)
        
        def _Degenerate(Q, R, S, inp):
            #print("Degenerate method")
            x1 = -2*np.cbrt(R.real)-inp[2]/3 
            x2 = np.cbrt(R.real)-inp[2]/3
            return (x1, x2, np.NaN)
        
        def _solve(inp): 
            #print(f"Input: {inp}")
            Q = (inp[2]**lc(2) - 3*inp[1])/9
            R = (2*inp[2]**3-9*inp[1]*inp[2]+27*inp[0])/54
            S = Q**3 - R**2
            #print(f"Q: {Q}, R: {R}, S: {S}")
            x1, x2, x3 = 0, 0, 0
            if np.isclose(0, S, lc(os.environ.get('tolerance', '1e-08'))):
                x1, x2, x3 = _Degenerate(Q, R, S, inp)
            elif S > 0:
                x1, x2, x3 = _Usual(Q, R, S, inp)
            else:
                x1, x2, x3 = _Complex(Q, R, S, inp)
            #print(f"Preresult: {x1}, {x2}, {x3} ")
            arr = [x1, x2, x3]
            return np.longcomplex(arr).reshape((3, ))

        newArray = np.apply_along_axis(_checkA, 1, self.array.values)
        newArray = np.apply_along_axis(_solve, 1, newArray)
        return Array(newArray)
