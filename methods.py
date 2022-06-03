from numpy import longdouble as ld
import numpy as np
def arsh(x):
    return np.log(x + np.sqrt(x**ld(2)+ld(1)))

def arch(x):
    return np.log(x - np.sqrt(x**ld(2)-ld(1)))

def sh(x):
    return (np.exp(x) - np.exp(-x))/ld(2)

def ch(x):
    return (np.exp(x) + np.exp(-x))/ld(2)

def arg(x, y):
    # Аргумент комплексного числа
    print(x, y)
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
