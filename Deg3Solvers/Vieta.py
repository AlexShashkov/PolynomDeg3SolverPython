from functools import singledispatch, update_wrapper
import numpy as np
from numpy import longcomplex as lc
from numpy import power as npow

np.seterr(all='raise')


class Solver(object):
    """
    Имплементация Тригонометрической формулы Виеты
    http://poivs.tsput.ru/ru/Math/Functions/Polynomials/VietaTrigonometricFormula
    """
    def __init__(self):
        self.pidiv3 = np.pi/3
        self.sqrt3 = np.sqrt(3)
        self.onethree = 1/3
    def __call__(self, array:"ndarray") -> "ndarray":
        """Функтор для решения уравнений методом Виета.

        @type array: ndarray
        @param array: Входной массив данных.
        @rtype: ndarray
        @returns: Объект типа ndarray с решениями уравнения.
        """
        self.array = array

        if self.array.shape[1] != 4:
            raise Exception("Wrong dimension. Vieta method works only with shapes of (N, 4)!")

        # Построчно вычислим корни
        newArray = np.apply_along_axis(self._checkA, 1, self.array)
        newArray = np.apply_along_axis(self._solve, 1, newArray)
        return newArray

    def _checkA(self, row) -> "ndarray":
        """Модификация строки входных данных.

        @type row: ndarray
        @param row: Строка входных данных.
        @rtype: ndarray
        @returns: Измененная строка.
        """
        newCol = row.copy()
        # В случае если число слишком маленькое, то из строки 9 будет вызвано исключение
        if row[3] != 0:
            newCol /= row[3]
        return newCol

    def _Usual(self, Q, R, S, inp) -> "ndarray":
        """Решение уравнения с действительными корнями

        @type Q: number
        @param inp: Полученный параметр Q
        @type S: number
        @param inp: Полученный параметр S
        @type R: number
        @param inp: Полученный параметр R
        @type inp: ndarray
        @param inp: Входной массив данных.
        @rtype: ndarray
        @returns: Объект типа ndarray с решениями уравнения.
        """
        inp2three = inp[2]*self.onethree
        phi = np.arccos(R/np.sqrt(Q[1]))*self.onethree

        sqrtQ = 2*np.sqrt(Q[0])
        x1 = -sqrtQ*np.cos(phi)-inp2three
        x2 = -sqrtQ*np.cos(phi+2*self.pidiv3)-inp2three
        x3 = -sqrtQ*np.cos(phi-2*self.pidiv3)-inp2three
        return (x1, x2, x3)

    def _Complex(self, Q, R, S, inp) -> "ndarray":
        """Решение уравнения с комплексными корнями

        @type Q: number
        @param inp: Полученный параметр Q
        @type S: number
        @param inp: Полученный параметр S
        @type R: number
        @param inp: Полученный параметр R
        @type inp: ndarray
        @param inp: Входной массив данных.
        @rtype: ndarray
        @returns: Объект типа ndarray с решениями уравнения.
        """
        inp2three = inp[2]*self.onethree
        phi, T = 0, 0
        x2, x3 = 0, 0
        absQ3 = np.abs(Q[1])
        sqrtabsQ = np.sqrt(np.abs(Q[0]))
        if Q[0]>0:
            phi = np.arccosh(np.abs(R)/np.sqrt(absQ3), dtype=np.complex)*self.onethree
            T = np.sign(R)*sqrtabsQ*np.cosh(phi)
            sqrtsh = self.sqrt3*sqrtabsQ*np.sinh(phi)
            Tin = T - inp2three
            sqrtsh *= 1j
            x2 = Tin + sqrtsh
            x3 = Tin - sqrtsh
        else:
            phi = np.arcsinh(np.abs(R)/np.sqrt(absQ3), dtype=np.complex)*self.onethree
            T = np.sign(R)*sqrtabsQ*np.sinh(phi)
            sqrtch = self.sqrt3*sqrtabsQ*np.cosh(phi)
            Tin = T - inp2three
            sqrtch *= 1j
            x2 = Tin + sqrtch
            x3 = Tin - sqrtch
        x1 = -2*T-inp2three
        return (x1, x2, x3)

    def _Degenerate(self, Q, R, S, inp) -> "ndarray":
        """Решение уравнения с действительными корнями в случае S = 0

        @type Q: number
        @param inp: Полученный параметр Q
        @type S: number
        @param inp: Полученный параметр S
        @type R: number
        @param inp: Полученный параметр R
        @type inp: ndarray
        @param inp: Входной массив данных.
        @rtype: ndarray
        @returns: Объект типа ndarray с решениями уравнения.
        """
        #print("Degenerate method")
        inp2three = inp[2]*self.onethree
        _x = np.cbrt(R.real)
        x1 = -2*_x-inp2three
        x2 = _x-inp2three
        return (x1, x2, np.NaN)

    def _solve(self, inp) -> "ndarray":
        """Соответственно вычисление корней. Вычисляются переменные Q, R и S по заданным формулам, после чего по параметру
            S определяется тип корней уравнения:
                * S >= 0: действительные корни.
                * S < 0: комплексные корни.

        @type inp: ndarray
        @param inp: Входной массив данных.
        @rtype: ndarray
        @returns: Объект типа ndarray с решениями уравнения.
        """
        Q = npow(inp[2], 2)*self.onethree*self.onethree - inp[1]*self.onethree
        x1, x2, x3 = 0, 0, 0
        if Q == 0:
            # Случай (x-a)^3
            x1, x2, x3 = [-inp[2]/3]*3
        else:
            R = npow(inp[2], 3)*self.onethree*self.onethree*self.onethree-inp[1]*inp[2]/6+inp[0]/2
            R2 = npow(R, 2)
            Q3 = npow(Q, 3)
            S = Q3 - R2
            if S == 0:
                x1, x2, x3 = self._Degenerate(Q, R, S, inp)
            elif S > 0:
                x1, x2, x3 = self._Usual([Q, Q3], R, S, inp)
            else:
                x1, x2, x3 = self._Complex([Q, Q3], R, S, inp)
            arr = [x1, x2, x3]
            return np.longcomplex(arr).reshape((3, ))

Solver__doc__ = "Решает уравнения третьей степени методом Виета. На вход принимает многомерный массив, длина строки - 4. Возвращает матрицу с решениями для каждой строки."
