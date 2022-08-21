from functools import reduce
from numpy import longdouble as ld
import numpy as np
from numpy.polynomial import polynomial as P
import random


def fastpow(x, deg):
    """ Быстрое возведение в степень для натуральных чисел
    https://en.wikipedia.org/wiki/Exponentiation_by_squaring
    Numpy решает все-равно быстрее
    @type x: int
    @param x: Число, которое необходимо возвести в степень.
    @type def: int
    @param deg: Непосредственно необходимая степень числа.
    @rtype: int
    @returns: Число x в степени deg
    """
    if x == 1 or x == 0:
        return x
    if deg == 0:
        return 1
    if deg < 0:
        return 1 / power(x, -deg)
    ans = 1
    while deg:
        if deg & 1:
            ans *= x
        deg >>= 1
        x *= x
    return ans

def generateEquationsFromReady(array:"Array") -> list:
    """ Сгенерировать коэффициенты полиномов по корням
    @type array: Array
    @param array: Массив из корней размерностью (N, 3)
    @rtype: list
    @returns: Трехмерный список из коэффицентов и корней
    """
    vals = np.apply_along_axis(P.polyfromroots, 1, array)
    return [vals, array]

def generateComplexEquations(count=10) -> list:
    """ Сгенерировать коэффициенты полиномов и комплексные корни
    @type count: int
    @param count: Количество полиномов
    @rtype: list
    @returns: Трехмерный список из коэффицентов и корней
    """
    # arr = np.random.randint(frm, to, (count, 3)).astype("float")
    arr = np.random.rand(count, 3) + np.random.rand(count, 3) * 1j

    return generateEquationsFromReady(arr)

def generateIntegerEquations(count=10, max=1, min=0) -> list:
    """ Сгенерировать коэффициенты полиномов и комплексные корни
    @type count: int
    @param count: Количество полиномов
    @type max: int
    @param count: Максимально возможный коень
    @type min: int
    @param count: Минимально возможный корень
    @rtype: list
    @returns: Трехмерный список из коэффицентов и корней
    """
    arr = np.random.randint(min, max, (count, 3)) + \
        np.random.randint(min, max, (count, 3))*1j
    return generateEquationsFromReady(arr)

def generateExponentComplexEquations(count=10, max=1, min=0) -> list:
    """ Сгенерировать коэффициенты полиномов и комплексные корни
    с помощью экспонент
    @type count: int
    @param count: Количество полиномов
    @type max: int
    @param count: Максимально возможная степень экспоненты
    @type min: int
    @param count: Минимально возможная степень экспоненты
    @rtype: list
    @returns: Трехмерный список из коэффицентов и корней
    """
    # arr = np.random.randint(frm, to, (count, 3)).astype("float")
    def rnd():
        exp = random.randint(min, max)
        significand = 0.9 * random.random() + 0.1
        return significand * 10**exp
    arr = []
    for i in range(count):
        arr.append([rnd() for _ in range(3)])
    arr = np.array(arr)

    carr = []
    for i in range(count):
        carr.append([rnd() for _ in range(3)])
    carr = np.array(arr)*1j
    arr = arr + carr
    return generateEquationsFromReady(arr)
