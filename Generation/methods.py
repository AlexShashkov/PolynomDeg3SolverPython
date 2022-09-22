from functools import reduce
from numpy import longdouble as ld
import numpy as np
from numpy.polynomial import polynomial as P
import random


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
    arr = np.random.rand(count, 3) + np.random.rand(count, 3) * 1j

    return generateEquationsFromReady(arr)

def generateIntegerEquations(count=10, max=9, min=0, coeff=1) -> list:
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
    # print("init arr", arr)
    arr *= coeff
    # print("init with small delimeter", arr)
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
