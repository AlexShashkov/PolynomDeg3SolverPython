import methods
from methods import arg
from functools import singledispatch, update_wrapper
from MethodsArray import Array, Struct
import numpy as np
from numpy import longcomplex as lc, power as npow
import os

class Solver(object):
    def __init__(self, array:"Array") -> "Array":
        self.round_dec = bool(os.environ.get('roundto', 1))
        self.array = Array(array)

        if self.array.shape[1] != 4:
            raise Exception("Wrong dimension. Baydoun method works only with shapes of (N, 4)!")

    def __call__(self) -> Array:
        newArray = np.apply_along_axis(self._checkA, 1, self.array.values)
        newArray = np.apply_along_axis(self._solve, 1, newArray)
        return Array(newArray)

    def _checkA(self, row):
        newCol = row.copy()
        print(row.shape)
        #print(row)
        if row[3] != lc(0):
            newCol /= row[3]
        a = newCol[3]
        b = newCol[2]
        c = newCol[1]
        d = newCol[0]

        b = Struct(init=b, deg2=npow(b, 2), \
                deg3=npow(b, 3), deg4=npow(b, 4), deg5=npow(b, 5), deg6=npow(b, 6), name="b")
        c = Struct(init=c, deg2=npow(c, 2), \
                deg3=npow(c, 3), deg4=npow(c, 4), name="c")
        d = Struct(init=d, deg2=npow(d, 2), \
                deg3=npow(d, 3), name="d")

        return np.array([d, c, b, a])

    def _part2(self, row, o, r):
        a = row[3]
        b = row[2]
        c = row[1]
        d = row[0]
        t = 2*c.deg3 * (8*b.deg6 + 132*b.deg3*d() +
            36*d.deg2 + c.deg3 + 33*b.deg2 *
            c.deg2 - 66*b()*c()*d()) + 12*b.deg4*c() * (d.deg2 -
            7*c.deg3) - b.deg2*c.deg2*d()*(24*b.deg3+291*d()) + d.deg3*(144*b()*c() - 2*d.deg3 - 27*d())
        d0 = 4*b.deg4*c.deg2 - 4*b.deg3*c()*d() - 14*b.deg2*c.deg3 + b.deg2*d.deg2 + 28*b()*c.deg2*d() + c.deg4 - 12*c()*d.deg2

        sqrt1 = None
        if o > 0:
            sqrt1 = npow(o + 0j, 1/2)
        else:
            sqrt1 = lc(0+1j)*npow(abs(o)+0j, 1/2)

        sqrt2 = lc(0+1j)*npow(lc(3), 1/2)
        sqrt3 = npow(lc(4), 1/3)

        bl = (d()-b()*c()) * sqrt1 * (4*b.deg2*c.deg2 - 4*b()*c()*d() + c.deg3 + d.deg2) + (sqrt2/9)*t
        bl1 = npow(bl, 1/3)
        bl2 = npow(bl, 2/3)
        A1 = (-2*sqrt2/3)*(4*b.deg3*c() - 2*d()*b.deg2 - 13*b()*c.deg2 + 15*d()*c()) + 2*c()*sqrt1
        A2 = 8*b.deg5*c.deg2 - 8*b.deg4*c()*d() - 40*b.deg3*c.deg3 + 2*b.deg3*d.deg2 + 116*b.deg2*c.deg2*d()
        A2 += 23*b()*c.deg4 - 99*b()*c()*d.deg2 - 21*c.deg3*d() + 27*d.deg3 - sqrt1*sqrt2 * (8*b.deg2*c.deg2 - 10*b()*c()*d() +
            c.deg3 + 3*d.deg2)

        R1 = None
        R2 = npow(sqrt1 * sqrt2 / 9 - r, 1/3)
        if o != 0:
            R1 = npow(sqrt1 * sqrt2 / 9 + r, 1/3)
        else:
            R1 = -R2

        # R1 = npow(sqrt1 * sqrt2 / 9 + r, 1/3)
        # R2 = npow(sqrt1 * sqrt2 / 9 - r, 1/3)
        print("R1, R2")
        print(R1, R2)

        M = [-1, 0.5 - sqrt2/2, 0.5 + sqrt2/2]
        M2 = [1, -0.5-sqrt2/2, -0.5 + sqrt2/2]

        print("args")
        arg1_1 = A1*bl1
        arg1_2 = -d0*R1
        arg2_1 = A2*bl2
        arg2_2 = npow(d0, 2)*R2
        print(arg1_1.real,arg1_1.imag)
        print(arg1_2.real, arg1_2.imag)
        print(arg2_1.real, arg2_1.imag)
        print(arg2_2.real,arg2_2.imag)

        phi1 = arg(arg1_1.real, arg1_1.imag) - arg(arg1_2.real, arg1_2.imag)
        phi2 = arg(arg2_1.real, arg2_1.imag) - arg(arg2_2.real, arg2_2.imag)

        a1 = (sqrt3/2)*(np.cos(phi1)+1j*np.sin(phi1))
        a2 = (sqrt3/2)*(np.cos(phi2)+1j*np.sin(phi2))

        print("alphas: ", a1, a2)
        print("M2:", M[2], M2[2])
        x1 = M[0]*a1*R1 + M2[0]*a2*R2 - b()/3
        x2 = M[1]*a1*R1 + M2[1]*a2*R2 - b()/3
        x3 = M[2]*a1*R1 + M2[2]*a2*R2 - b()/3
        return [x1, x2, x3]


    def _solve(self, row):
        a = row[3]
        b = row[2]
        c = row[1]
        d = row[0]
        o = -4*b.deg3*d() + b.deg2*c.deg2 + 18*b()*c()*d() - 4*c.deg3 - 27*d.deg2
        r = (2*b.deg3 - 9*b()*c() + 27*d())/27
        arr = None
        if o == 0 and r ==0:
            x1 = x2 = x3 = -b()/3
            arr = [x1, x2, x3]
        else:
            arr = self._part2(row, o, r)
        return np.longcomplex(arr).reshape((3, ))

