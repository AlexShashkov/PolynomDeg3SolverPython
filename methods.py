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
    if x > 0 and y >= 0:
        return np.arctan(y/x)
    elif x < 0 and y >= 0:
        return np.pi - np.arctan(np.absolute(y/x))
    elif  x < 0 and y < 0:
        return np.pi + np.arctan(np.absolute(y/x))
    elif x > 0 and y < 0:
        return 2*np.pi - np.arctan(np.absolute(y/x))
    elif x == 0 and y > 0:
        return np.pi/2
    elif x == 0 and y < 0:
        return (3*np.pi)/2
    elif x == 0 and y == 0:
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
    if deg < 0:
        return 1 / power(x, -deg)
    ans = 1
    while deg:
        if deg & 1:
            ans *= x
        deg >>= 1
        x *= x
    return ans

