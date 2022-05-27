from types import SimpleNamespace

import methods
from numpy import longdouble as ld, cbrt, longcomplex as lc, power as npow
import numpy as np

def arg(x, y):
    # Аргумент комплексного числа
    if x >= 0 and y >= 0:
        return np.arctan(x/y)
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
    else:
        raise ValueError("Invalid type of complex z")

class Struct(SimpleNamespace):
    # Для хранения степеней числа
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def __call__(self):
        return self.init
    def expand(self, **kwargs):
        for key, value in kwargs.items():
            #print(key, value)
            #vars()[key] = value
            setattr(self, key, value)


sqrt1 = npow(lc(0), 1/2)
sqrt2 = lc(0+1j)*npow(3, 1/2)
sqrt3 = npow(lc(4), 1/3)
sqrt6 = npow(3, 2/3)/2


inp = [lc(0)]*4
inp[3] = lc(input("Введите число при x³ > "))
inp[2] = lc(input("Введите число при x² > "))
inp[1] = lc(input("Введите число при x > "))
inp[0] = lc(input("Введите свободный член > "))

if inp[3]!=lc(1):
    #3 Если еоэффициент при x степени 3 не равен 1
	item = inp[3].copy()
	inp = lc(list(map(lambda x: x/item, inp)))
print("Input: ", inp)

a, b, c, d = inp
b = Struct(init=b, deg2=npow(b,2), deg3=npow(b, 3))
c = Struct(init=c, deg2=npow(c, 2), deg3=npow(c, 3))
d = Struct(init=d, deg2=npow(d, 2))
b.expand(deg4=npow(b(), 4), deg5=npow(b(), 5), deg6=npow(b(), 6))
c.expand(deg4=npow(c(), 4))
d.expand(deg3=npow(d(), 3))


o = -4*b.deg2*d + b.deg2*c.deg2 + 18*b()*c()*d() - 4*c.deg3 - 27*d.deg2
d0 = 4*b.deg4*c.deg2 - 4*b.deg3*c()*d() - 14*b.deg2*c.deg3 + b.deg2*d.deg2 + 28*b()*c.deg2*d() + c.deg4 - 12*c()*d.deg2
print(o, d0)


r = (2*b.deg3 - 9*b()*c() + 27*d())/27
R1 = npow((sqrt2/9)*sqrt1+r, 1/3)
R2 = npow((sqrt2/9)*sqrt1-r, 1/3)

x1 = x2 = x3 = None

# METHOD 1
if o == 0 and r ==0:
    x1 = x2 = x3 = -b()/3
else:
    t = 2*c.deg3 * (8*b.deg6 + 132*b.deg3*d() +
        36*d.deg2 + c.deg3 + 33*b.deg2 *
        c.deg2 - 66*b()*c()*d()) + 12*b.deg4*c() * (d.deg2 -
        7*c.deg3) - b.deg2*c.deg2*d()*(24*b.deg3+291*d()) + d.deg3*(144*b()*c() - 2*d.deg3 - 27*d())


    bl = (d()-b()*c()) * sqrt1 * (4*b.deg2*c.deg2 - 4*b()*c()*d() + 2*c.deg3 + d.deg2) + (sqrt2/9)*t
    bl1 = npow(bl, 1/3)
    bl2 = npow(bl, 2)

    A1 = (-2*sqrt2/3)*(4*b.deg3*c() - 2*d()*b.deg2 - 13*b()*c.deg2 + 15*d()*c()) + 2*c()*sqrt1
    A2 = 8*b.deg5*c.deg2 - 8*b.deg4*c()*d() - 40*b.deg3*c.deg3 + 2*b.deg3*d.deg2 + 116*b.deg2*c.deg2*d()
    A2 += 23*b()*c.deg4 - 99*b()*c()*d.deg2 - 21*c.deg3*d() + 27*d.deg3 - sqrt1*sqrt2 * (8*b.deg2*c.deg2 - 10*b()*c()*d() +
        c.deg3 + 3*d.deg2)
    arg1_1 = A1*bl1
    arg1_2 = -d0*R1
    arg2_1 = A2*bl2
    arg2_2 = npow(d0, 2)*R2
    phi1 = arg(arg1_1.real, arg1_1.imag) - arg(arg1_2.real, arg1_2.imag)
    phi2 = arg(arg2_1.real, arg2_1.imag) - arg(arg2_2.real, arg2_2.imag)
    a1 = sqrt3*(np.cos(phi1)+1j*np.sin(phi1))
    a2 = sqrt3*(np.cos(phi2)+1j*np.sin(phi2))
    M = [-1, 0.5 - sqrt2/2, 0.5 + sqrt2/2]
    M2 = [1, -0.5-sqrt2/2, 0.5+ sqrt2/2]
    x1 = M[0]*a1*R1 + M2[0]*a2*R2 - b()/3
    x2 = M[1]*a1*R1 + M2[1]*a2*R2 - b()/3
    x3 = M[2]*a1*R1 + M2[2]*a2*R2 - b()/3
print(x1, x2, x3)
