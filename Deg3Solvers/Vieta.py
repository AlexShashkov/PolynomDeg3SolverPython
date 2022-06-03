import methods
from functools import singledispatch, update_wrapper
from MethodsArray import Array
import numpy as np
from numpy import longcomplex as lc
import os

class Solver(object):
    def __call__(self, array:"Array") -> "Array":
        """Функтор для решения уравнений методом Виета.

        @type array: Array
        @param array: Входной массив данных. Может быть обычным массивом, массивом NumPy
            или модифицированным Array.
        @rtype: Array
        @returns: Объект типа Array с решениями уравнения.
        """
        self.round_dec = bool(os.environ.get('roundto', 1))
        self.array = Array(array)

        if self.array.shape[1] != 4:
            raise Exception("Wrong dimension. Vieta method works only with shapes of (1, 4)!")

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
        phi = np.arccos(R/np.sqrt(Q**3))/3
        #print("Usual method")
        #print(f"Phi: {phi} ")
        x1 = -2*np.sqrt(Q)*np.cos(phi)-inp[2]/3
        x2 = 2*np.sqrt(Q)*np.cos(phi+2*np.pi/3)-inp[2]/3
        x3 = -2*np.sqrt(Q)*np.cos(phi-2*np.pi/3)-inp[2]/3
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
        x1 = -2*np.cbrt(R.real)-inp[2]/3
        x2 = np.cbrt(R.real)-inp[2]/3
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
        Q = (inp[2]**lc(2) - 3*inp[1])/9
        R = (2*inp[2]**3-9*inp[1]*inp[2]+27*inp[0])/54
        S = Q**3 - R**2
        #print(f"Q: {Q}, R: {R}, S: {S}")
        x1, x2, x3 = 0, 0, 0
        if np.isclose(0, S, lc(os.environ.get('tolerance', '1e-08'))):
            x1, x2, x3 = self._Degenerate(Q, R, S, inp)
        elif S > 0:
            x1, x2, x3 = self._Usual(Q, R, S, inp)
        else:
            x1, x2, x3 = self._Complex(Q, R, S, inp)
        #print(f"Preresult: {x1}, {x2}, {x3} ")
        arr = [x1, x2, x3]
        return np.longcomplex(arr).reshape((3, ))

Solver__doc__ = "Решает уравнения третьей степени методом Виета. На вход принимает многомерный массив, длина строки - 4. Возвращает матрицу с решениями для каждой строки."
