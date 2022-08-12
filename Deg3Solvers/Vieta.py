import methods
from methods import fastpow as fpow
from functools import singledispatch, update_wrapper
from MethodsArray import Array
import numpy as np
from numpy import longcomplex as lc
from numpy import power as npow

np.seterr(all='raise')


class Solver(object):
    def __init__(self):
        self.pidiv3 = np.pi/3
        self.sqrt3 = np.sqrt(3)
    def __call__(self, array:"Array") -> "Array":
        """Функтор для решения уравнений методом Виета.

        @type array: Array
        @param array: Входной массив данных. Может быть обычным массивом, массивом NumPy
            или модифицированным Array.
        @rtype: Array
        @returns: Объект типа Array с решениями уравнения.
        """
        self.array = Array(array)

        if self.array.shape[1] != 4:
            raise Exception("Wrong dimension. Vieta method works only with shapes of (N, 4)!")

        # Построчно вычислим корни
        newArray = np.apply_along_axis(self._checkA, 1, self.array.values)
        newArray = np.apply_along_axis(self._solve, 1, newArray)
        return Array(newArray)

    def _checkA(self, row):
        """Модификация строки входных данных.

        @type row: Array
        @param row: Строка входных данных.
        @rtype: Array
        @returns: Измененная строка.
        """
        newCol = row.copy()
        #print(row)
        # В случае если число слишком маленькое, то из строки 9 будет вызвано исключение
        if row[3] != 0:
            newCol /= row[3]
        #print(newCol)
        return newCol

    def _Usual(self, Q, R, S, inp):
        """Решение уравнения с действительными корнями

        @type Q: number
        @param inp: Полученный параметр Q
        @type S: number
        @param inp: Полученный параметр S
        @type R: number
        @param inp: Полученный параметр R
        @type inp: Array
        @param inp: Входной массив данных. Может быть обычным массивом, массивом NumPy
            или модифицированным Array.
        @rtype: Array
        @returns: Объект типа Array с решениями уравнения.
        """
        inp2three = inp[2]/3

        phi = np.arccos(R/np.sqrt(Q[1]))/3
        #print("Usual method")
        #print(f"Phi: {phi} ")

        sqrtQ = 2*np.sqrt(Q[0])
        x1 = -sqrtQ*np.cos(phi)-inp2three
        x2 = sqrtQ*np.cos(phi+2*self.pidiv3)-inp2three
        x3 = -sqrtQ*np.cos(phi-2*self.pidiv3)-inp2three
        return (x1, x2, x3)

    def _Complex(self, Q, R, S, inp):
        """Решение уравнения с комплексными корнями

        @type Q: number
        @param inp: Полученный параметр Q
        @type S: number
        @param inp: Полученный параметр S
        @type R: number
        @param inp: Полученный параметр R
        @type inp: Array
        @param inp: Входной массив данных. Может быть обычным массивом, массивом NumPy
            или модифицированным Array.
        @rtype: Array
        @returns: Объект типа Array с решениями уравнения.
        """
        #print("Complex method")
        inp2three = inp[2]/3
        phi = 0
        T = 0
        x2, x3 = 0, 0
        absQ3 = np.abs(Q[1])
        sqrtabsQ = np.sqrt(np.abs(Q[0]))
        if Q[0]>0:
            phi = methods.arch(np.abs(R)/np.sqrt(absQ3))/3
            T = np.sign(R)*sqrtabsQ*methods.ch(phi)
            sqrtsh = self.sqrt3*sqrtabsQ*methods.sh(phi)
            x2 = T -inp2three +1j*sqrtsh
            x3 = T -inp2three -1j*sqrtsh
        else:
            phi = methods.arsh(np.abs(R)/np.sqrt(np.abs(Q[1])))/3
            T = np.sign(R)*sqrtabsQ*methods.sh(phi)
            sqrtch = self.sqrt3*sqrtabsQ*methods.ch(phi)
            x2 = T -inp2three + 1j*sqrtch
            x3 = T -inp2three - 1j*sqrtch
        #print(f"Phi: {phi}, T: {T}")
        x1 = -2*T-inp2three
        return (x1, x2, x3)

    def _Degenerate(self, Q, R, S, inp):
        """Решение уравнения с действительными корнями в случае S = 0

        @type Q: number
        @param inp: Полученный параметр Q
        @type S: number
        @param inp: Полученный параметр S
        @type R: number
        @param inp: Полученный параметр R
        @type inp: Array
        @param inp: Входной массив данных. Может быть обычным массивом, массивом NumPy
            или модифицированным Array.
        @rtype: Array
        @returns: Объект типа Array с решениями уравнения.
        """
        #print("Degenerate method")
        inp2three = inp[2]/3
        x1 = -2*np.cbrt(R.real)-inp2three
        x2 = np.cbrt(R.real)-inp2three
        return (x1, x2, np.NaN)

    def _solve(self, inp):
        """Соответственно вычисление корней. Вычисляются переменные Q, R и S по заданным формулам, после чего по параметру
            S определяется тип корней уравнения:
                * S >= 0: действительные корни.
                * S < 0: комплексные корни.

        @type inp: Array
        @param inp: Входной массив данных. Может быть обычным массивом, массивом NumPy
            или модифицированным Array.
        @rtype: Array
        @returns: Объект типа Array с решениями уравнения.
        """
        #print(f"Input: {inp}")
        Q = (fpow(inp[2], 2) - 3*inp[1])/9
        R = (2*fpow(inp[2], 3)-9*inp[1]*inp[2]+27*inp[0])/54
        Q3 = npow(Q, 3)
        R2 = npow(R, 2)
        S = Q3 - R2
        #print(f"Q: {Q}, R: {R}, S: {S}")
        x1, x2, x3 = 0, 0, 0
        if S == 0:
            x1, x2, x3 = self._Degenerate(Q, R, S, inp)
        elif S > 0:
            x1, x2, x3 = self._Usual([Q, Q3], R, S, inp)
        else:
            x1, x2, x3 = self._Complex([Q, Q3], R, S, inp)
        #print(f"Preresult: {x1}, {x2}, {x3} ")
        arr = [x1, x2, x3]
        return np.longcomplex(arr).reshape((3, ))

Solver__doc__ = "Решает уравнения третьей степени методом Виета. На вход принимает многомерный массив, длина строки - 4. Возвращает матрицу с решениями для каждой строки."
