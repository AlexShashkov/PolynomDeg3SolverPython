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
