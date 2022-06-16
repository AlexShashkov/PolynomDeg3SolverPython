from functools import reduce
from numpy import longdouble as ld
import numpy as np
def arsh(x):
    """ Аршинус
    @param x: От чего необходимо вычислить аршинус
    """
    return np.log(x + np.sqrt(x**ld(2)+ld(1)))

def arch(x):
    """ Аркошинус
    @param x: От чего необходимо вычислить аркошинус
    """
    return np.log(x - np.sqrt(x**ld(2)-ld(1)))

def sh(x):
    """ Шинус
    @param x: От чего необходимо вычислить шинус
    """
    return (np.exp(x) - np.exp(-x))/ld(2)

def ch(x):
    """ Кошинус
    @param x: От чего необходимо вычислить кошинус
    """
    return (np.exp(x) + np.exp(-x))/ld(2)

def arg(x, y):
    """ Аргумент комплексного числа
    @type x: number
    @param x: Действительная часть
    @type y: number
    @param y: Мнимая часть
    """
    if x > 0:
        if y >= 0:
            return np.arctan(y/x)
        else:
            return 2*np.pi - np.arctan(np.absolute(y/x))
    elif x < 0:
        if y >= 0:
            return np.pi - np.arctan(np.absolute(y/x))
        else:
            return np.pi + np.arctan(np.absolute(y/x))
    elif x == 0:
        if y > 0:
            return np.pi/2
        elif y < 0:
            return (3*np.pi)/2
        else:
            return 0
    else:
        raise ValueError("Invalid type of complex z")

def fastpow(x, deg):
    """ Быстрое возведение в степень для натуральных чисел
    https://en.wikipedia.org/wiki/Exponentiation_by_squaring
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

def geneq(args:"Array") -> "Array":
    # print("workng with row", args)
    def _mul(x):
        return x[0]*x[1]
    """ Генерация полинома третьей степени
    @type args: Array
    @param args: Корни полинома
    @rtype: Array
    @returns: Коэффициенты полинома для заданных корней
    """
    # X^3 : 1
    # X^2
    X = reduce(lambda x,y: x + y, args)
    #X
    Y = _mul(args[:2]) +  _mul(args[1:]) + _mul(args[0::2])
    # C
    Z = reduce(lambda x, y: x*y, args)
    return [Z, Y, X, 1]


def generateEquationsFromReady(array:"Array") -> list:
    """ Сгенерировать коэффициенты полиномов по корням
    @type array: Array
    @param array: Массив из корней размерностью (N, 3)
    @rtype: list
    @returns: Трехмерный список из коэффицентов и корней
    """
    vals = np.apply_along_axis(geneq, 1, array)
    return [vals, array]


def generateEquations(count=10, frm=0, to=100) -> list:
    """ Сгенерировать коэффициенты полиномов и корни
    @type count: int
    @param count: Количество полиномов
    @type frm: int
    @param count: Минимальное значение корня
    @type to: int
    @param count: Максимальное значение корня
    @rtype: list
    @returns: Трехмерный список из коэффицентов и корней
    """
    arr = np.random.randint(frm+1, to+1, (count, 3)).astype("float")

    return generateEquationsFromReady(arr)
