import methods
from functools import singledispatch, update_wrapper
from MethodsArray import Array
import numpy as np
from numpy import longcomplex as lc
import os

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
