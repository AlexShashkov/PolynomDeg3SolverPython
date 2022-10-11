from functools import singledispatch, update_wrapper
import numpy as np
from numpy import longcomplex as lc, power as npow
import os

np.seterr(all='raise')

class Solver(object):
    """
    Имплементация 'Analytical formula for the roots of the general complex cubic polynomial'
    Автор: Ibrahim Baydoun
    Статья: https://arxiv.org/abs/1512.07585
    """
    def __init__(self):
        self.onethree = 1/3
        self.twothree = self.onethree*2
        self.sqrt3 = np.sqrt(3)
        self.cbrt4 = np.cbrt(4)

    def __call__(self, array:"ndarray") -> "ndarray":
        """Функтор для решения уравнений методом Baydoun.
        @type array: ndarray
        @param array: Входной массив данных.
        @rtype: ndarray
        @returns: Объект типа ndarray с решениями уравнения.
        """
        self.array = array
        if self.array.ndim == 1:
            self.array = self.array.reshape((1, self.array.shape[0]))

        if self.array.shape[1] != 4:
            raise Exception("Wrong dimension. Baydoun method works only with shapes of (N, 4)!")

        newArray = np.apply_along_axis(self._checkA, 1, self.array) #.values)
        newArray = np.apply_along_axis(self._solve, 1, newArray)
        return newArray #Array(newArray)

    def _checkA(self, row) -> "ndarray":
        """Модификация строки входных данных. Вычисление вспомогательных степеней.
        @type row: ndarray
        @param row: Строка входных данных.
        @rtype: ndarray
        @returns: Измененная строка с вычисленными степенями.
        """
        newCol = row.copy()
        # В случае если число настолько маленькое и может вызвать переполнение, приведя к inf, то появится исключение из строки 9.
        if row[3] != lc(0):
            divThrid = 1/row[3]
            newCol *= divThrid
        a, b, c, d = newCol[3], newCol[2], newCol[1], newCol[0]
        b_arr, c_arr, d_arr = [b], [c], [d]
        for i in range(5):
            b_arr.append(b_arr[i]*b_arr[0])
        for i in range(3):
            c_arr.append(c_arr[i]*c_arr[0])
        for i in range(2):
            d_arr.append(d_arr[i]*d_arr[0])
        return np.array([d_arr, c_arr, b_arr, a], dtype=object)

    def _part2(self, row, o, r) -> "ndarray":
        """ Вычисление корней для случая, когда o != r.
        @type row: ndarray
        @param row: Входная строка.
        @type o: number
        @param o: Полученный параметр o.
        @type r: number
        @param r: Полученный параметр r.
        @rtype: ndarray
        @returns: Решения уравнения.
        """

        a, b, c, d = row[::-1]
        c0d0 = c[0]*d[0]
        b0c0 = b[0]*c[0]
        b0c1 = b[0]*c[1]
        b1c1 = b[1]*c[1]*4
        t = 2*c[2] * (4*(2*b[5] + 9*d[1]) + 33*(4*b[2]*d[0]  + b[1]*c[1] - \
            2*b[0]*c0d0) + c[2] ) + 12*b[3]*c[0] * (d[1] - 7*c[2]) - b[1] * \
            c[1]*d[0]*(24*b[2]+291*d[0]) + d[2]*(3*(48*b0c0 - 9*d[0]) - 2*b[2])
        d0 = 4*(b[3]*c[1] - b[2]*c0d0 - 3*c[0]*d[1]) + 14*(-b[1]*c[2] + \
                2*b0c1*d[0]) + b[1]*d[1] + c[3]
        sqrt1 = None
        if o > 0:
            sqrt1 = npow(o + 0j, 0.5)
        else:
            sqrt1 = lc(0+1j)*npow(abs(o)+0j, 0.5)
        sqrt2 = lc(0+1j)*self.sqrt3
        sqrt3 = lc(self.cbrt4)

        sqrt2div3 = sqrt2*self.onethree
        sqrt2div9 = sqrt2*self.onethree*self.onethree
        sqrt3ftwo = sqrt3*0.5

        bl = (d[0]-b0c0) * sqrt1 * (b1c1 - 2*(2*b[0]*c0d0 - c[2]) + d[1]) + (sqrt2div9)*t
        bl1 = npow(bl, self.onethree)
        bl2 = npow(bl1, 2)
        A1 = 2*((-sqrt2div3)*(2*(2*b[2]*c[0] - d[0]*b[1]) - 13*b0c1 + 15*c0d0) + c[0]*sqrt1)
        A2 = 8*(b[4]*c[1] - b[3]*c0d0 - 5*b[2]*c[2]) + 2*b[2]*d[1] +\
            29*b1c1*d[0] + 23*b[0]*c[3] +3*(-7*c[2]*d[0] +\
            3*(3*d[2] - 11*b0c0*d[1])) -sqrt1*sqrt2 * (2*(b1c1 - 5*b[0]*c0d0) + c[2] + 3*d[1])
        Rbase = sqrt1 * sqrt2div9
        R1 = None
        R2 = None
        if o == 0:
            if r > 0:
                R1 = npow(Rbase + r, self.onethree)
                R2 = -R1
            else:
                R2 = npow(Rbase - r, self.onethree)
                R1 = -R2
        else:
            R1 = npow(Rbase + r, self.onethree)
            R2 = npow(Rbase - r, self.onethree)


        sqrt205=sqrt2*0.5
        M = [-1, 0.5 - sqrt205, 0.5 + sqrt205]
        M2 = [1, -0.5 - sqrt205, -0.5 + sqrt205]

        arg1_1 = A1*bl1
        arg1_2 = -d0*R1
        arg2_1 = A2*bl2
        arg2_2 = npow(d0, 2)*R2

        # Вычисляем аргумент комплексного числа
        phi1 = np.angle(arg1_1) - np.angle(arg1_2)
        phi2 = np.angle(arg2_1) - np.angle(arg2_2)

        a1 = (sqrt3ftwo)*(np.cos(phi1)+1j*np.sin(phi1))
        a2 = (sqrt3ftwo)*(np.cos(phi2)+1j*np.sin(phi2))

        a1R1 = a1*R1
        a2R2 = a2*R2
        x1 = M[0]*a1R1 + M2[0]*a2R2 - self.bthree
        x2 = M[1]*a1R1 + M2[1]*a2R2 - self.bthree
        x3 = M[2]*a1R1 + M2[2]*a2R2 - self.bthree
        return [x1, x2, x3]


    def _solve(self, row) -> "ndarray":
        """
        Соответственно вычисление корней. Вычисляются переменные o и r по заданным формулам, после чего определяется тип корней уравнения:
        * o = r = 0 - действительные корни. Кратность хотя бы одного корня > 1.
        @type row: ndarray
        @param row: Входная строка.
        @rtype: ndarray
        @returns: Решения уравнения.
        """

        a, b, c, d = row[::-1]
        self.bthree = b[0]*self.onethree
        o = -4*(b[2]*d[0] + c[2]) + b[1]*c[1] + 9*(2*b[0]*c[0]*d[0] - 3*d[1])
        r = (2*b[2] + 9*(-b[0]*c[0] + 3*d[0]))/27
        arr = None
        if o == 0 and r == 0:
            # Стандартные действительные корни
            x1 = x2 = x3 = -self.bthree
            arr = [x1, x2, x3]
        else:
            # Используем другую формулу из статьи
            arr = self._part2(row, o, r)
        return np.longcomplex(arr).reshape((3, ))
Solver__doc__ = "Решает уравнения третьей степени методом Baydoun. На вход принимает многомерный массив, длина строки - 4. Возвращает матрицу с решениями для каждой строки."
