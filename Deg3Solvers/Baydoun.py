import methods
from methods import arg, fastpow as fpow
from functools import singledispatch, update_wrapper
from MethodsArray import Array, Struct, profile
import numpy as np
from numpy import longcomplex as lc, power as npow
import os

np.seterr(all='raise')

class Solver(object):
    def __init__(self):
        self.onethree = 1/3
        self.onenine = self.onethree * self.onethree
        self.one27 = self.onenine * self.onethree

        self.twothree = self.onethree*2
        self.sqrt3 = np.sqrt(3)
        self.cbrt4 = np.cbrt(4)
    def __call__(self, array:"Array") -> "Array":
        """Функтор для решения уравнений методом Baydoun.
        @type array: Array
        @param array: Входной массив данных. Может быть обычным массивом, массивом NumPy
            или модифицированным Array.
        @rtype: Array
        @returns: Объект типа Array с решениями уравнения.
        """
        self.array = Array(array)

        if self.array.shape[1] != 4:
            raise Exception("Wrong dimension. Baydoun method works only with shapes of (N, 4)!")

        newArray = np.apply_along_axis(self._checkA, 1, self.array.values)
        newArray = np.apply_along_axis(self._solve, 1, newArray)
        return Array(newArray)

    # @profile(strip_dirs=True)
    def _checkA(self, row):
        """Модификация строки входных данных. Вычисление вспомогательных степеней.
        @type row: Array
        @param row: Строка входных данных.
        @rtype: Array
        @returns: Измененная строка с вычисленными степенями.
        """
        newCol = row.copy()
        # print(row.shape)
        # vseprint(row)
        # В случае если число настолько маленькое и может вызвать переполнение, приведя к inf, то появится исключение из строки 9.
        if row[3] != lc(0):
            divThrid = 1/row[3]
            newCol *= divThrid
        a = newCol[3]
        b = newCol[2]
        c = newCol[1]
        d = newCol[0]

        # Вычислим степени с помощью fastpow 
        # Заменить на numpy.pow, т.к. все-равно реализация на c++ быстрее
        b_arr = [b]
        c_arr = [c]
        d_arr = [d]
        degs = [i for i in range(2, 7)]
        # print(degs[:4])
        # map замениить на цикл, который будет умножать на предыдущее значение
        b_arr.extend(list(map(lambda x, deg: fpow(x, deg), [b for i in range(5)], degs)))
        c_arr.extend(list(map(lambda x, deg: fpow(x, deg), [c for i in range(5)], degs[:3])))
        d_arr.extend(list(map(lambda x, deg: fpow(x, deg), [d for i in range(5)], degs[:2])))
        # print("b", b_arr, "\nc", c_arr, "\nd", d_arr, "\na", a)
        return np.array([d_arr, c_arr, b_arr, a], dtype=object)

    # @profile(strip_dirs=True)
    def _part2(self, row, o, r):
        """ Вычисление корней для случая, когда o != r.

        @type row: Array
        @param row: Входная строка.
        @type o: number
        @param o: Полученный параметр o.
        @type r: number
        @param r: Полученный параметр r.
        @rtype: Array
        @returns: Решения уравнения.
        """

        a = row[3]
        b = row[2]
        c = row[1]
        d = row[0]
        # print("o:", o)
        # print("r:", r)
        c0d0 = c[0]*d[0]
        b0c0 = b[0]*c[0]
        b0c1 = b[0]*c[1]
        b1c1 = b[1]*c[1]*4
        t = 2*c[2] * (8*b[5] + 132*b[2]*d[0] + 36*d[1] + c[2] + 33*b[1] * \
            c[1] - 66*b[0]*c0d0) + 12*b[3]*c[0] * (d[1] - 7*c[2]) - b[1] * \
            c[1]*d[0]*(24*b[2]+291*d[0]) + d[2]*(144*b0c0 - 2*b[2] - 27*d[0])
        d0 = 4*b[3]*c[1] - 4*b[2]*c0d0 - 14*b[1]*c[2] + b[1]*d[1] + 28*b0c1*d[0] + c[3] - 12*c[0]*d[1]

        sqrt1 = None
        # Это точно правильно?
        if o > 0:
            sqrt1 = npow(o + 0j, 0.5)
        else:
            sqrt1 = lc(0+1j)*npow(abs(o)+0j, 0.5)
        # Тоже сомнения
        sqrt2 = lc(0+1j)*self.sqrt3
        sqrt3 = lc(self.cbrt4)

        sqrt2div3 = sqrt2*self.onethree
        sqrt2div9 = sqrt2*self.onenine

        sqrt2ftwo = sqrt2*0.5
        sqrt3ftwo = sqrt3*0.5

        bl = (d[0]-b0c0) * sqrt1 * (b1c1 - 4*b[0]*c0d0 + 2*c[2] + d[1]) + (sqrt2div9)*t
        # print(bl)
        # Numpy cubic root не работает с комплексными числами.
        bl1 = npow(bl, self.onethree)
        bl2 = npow(bl1, 2)
        A1 = (-2*sqrt2div3)*(4*b[2]*c[0] - 2*d[0]*b[1] - 13*b0c1 + 15*c0d0) + 2*c[0]*sqrt1
        A2 = 8*b[4]*c[1] - 8*b[3]*c0d0 - 40*b[2]*c[2] + 2*b[2]*d[1] + 29*b1c1*d[0] #Че  за хуйня?1
        A2 += 23*b[0]*c[3] - 99*b0c0*d[1] - 21*c[2]*d[0] + 27*d[2] -\
        sqrt1*sqrt2 * (2*b1c1 - 10*b[0]*c0d0 + c[2] + 3*d[1])

        Rbase = sqrt1 * sqrt2div9
        #print(Rbase)
        #print(r)
        # Numpy cubic root не работает с комплексными числами.
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

        #print(R1, R2)


        M = [-1, 0.5 - sqrt2ftwo, 0.5 + sqrt2ftwo]
        M2 = [1, -0.5 - sqrt2ftwo, -0.5 + sqrt2ftwo]

        # print("args")
        arg1_1 = A1*bl1
        arg1_2 = -d0*R1
        arg2_1 = A2*bl2
        arg2_2 = npow(d0, 2)*R2
        # print(arg1_1.real,arg1_1.imag)
        # print(arg1_2.real, arg1_2.imag)
        # print(arg2_1.real, arg2_1.imag)
        # print(arg2_2.real,arg2_2.imag)

        # Вычисляем аргумент комплексного числа
        print("Argument of complex numbers")
        print(arg1_1, arg(arg1_1.real, arg1_1.imag), "vs", np.angle(arg1_1))
        print(arg1_2, arg(arg1_2.real, arg1_2.imag), "vs", np.angle(arg1_2))
        print(arg2_1, arg(arg2_1.real, arg2_1.imag), "vs", np.angle(arg2_1))
        print(arg2_2, arg(arg2_2.real, arg2_2.imag), "vs", np.angle(arg2_2))
        phi1 = np.angle(arg1_1) - np.angle(arg1_2)
        phi2 = np.angle(arg2_1) - np.angle(arg2_2)


        a1 = (sqrt3ftwo)*(np.cos(phi1)+1j*np.sin(phi1))
        a2 = (sqrt3ftwo)*(np.cos(phi2)+1j*np.sin(phi2))

        # print("alphas: ", a1, a2)
        # print("M2:", M[2], M2[2])
        a1R1 = a1*R1
        a2R2 = a2*R2
        x1 = M[0]*a1R1 + M2[0]*a2R2 - self.bthree
        x2 = M[1]*a1R1 + M2[1]*a2R2 - self.bthree
        x3 = M[2]*a1R1 + M2[2]*a2R2 - self.bthree

        if o>=0:
        # зануляем мнимую часть корней(тк все корни у нас 100% действительные)
            x1 = x1.real + 0j
            x2 = x2.real + 0j
            x3 = x3.real + 0j
        return [x1, x2, x3]


    def _solve(self, row):
        """Соответственно вычисление корней. Вычисляются переменные o и r по заданным формулам, после чего определяется тип корней уравнения:
                * o = r = 0 - действительные корни. Кратность хотя бы одного корня > 1.
                *
                    * o > 0 - Все корни действительные, кратность каждого 1.
                    * o < 0 - один действительный и два комплексных корня.
        @type row: Array
        @param row: Входная строка.
        @rtype: Array
        @returns: Решения уравнения.
        """

        a = row[3]
        b = row[2]
        c = row[1]
        d = row[0]


        self.bthree = b[0]*self.onethree
        # print("values:")
        # print(b)
        # print(c)
        # print(d)
        o = -4*b[2]*d[0] + b[1]*c[1] + 18*b[0]*c[0]*d[0] - 4*c[2] - 27*d[1]
        r = (2*b[2] - 9*b[0]*c[0] + 27*d[0])*self.one27
        arr = None
        if o == 0 and r ==0:
            print("Действительные корни")
            # Стандартные действительные корни
            x1 = x2 = x3 = -self.bthree
            arr = [x1, x2, x3]
        else:
            # Используем другую формулу из статьи
            arr = self._part2(row, o, r)
        return np.longcomplex(arr).reshape((3, ))
Solver__doc__ = "Решает уравнения третьей степени методом Baydoun. На вход принимает многомерный массив, длина строки - 4. Возвращает матрицу с решениями для каждой строки."
