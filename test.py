from types import SimpleNamespace

import methods
from numpy import longdouble as ld, cbrt, longcomplex as lc, power as npow
import numpy as np

class Struct(SimpleNamespace):
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
sqrt2 = npow(lc(-3), 1/2)
sqrt3 = npow(lc(4), 1/3)


inp = [lc(0)]*4
inp[3] = lc(input("Введите число при x³ > "))
inp[2] = lc(input("Введите число при x² > "))
inp[1] = lc(input("Введите число при x > "))
inp[0] = lc(input("Введите свободный член > "))

if inp[3]!=lc(1):
	item = inp[3].copy()
	inp = lc(list(map(lambda x: x/item, inp)))
print("Input: ", inp)

a, b, c, d = inp

print(d, c, b, a)

t = 2*npow(c, 3) * (8*npow(b, 6) + 132*npow(b, 3)*d +
        36*npow(d, 2) + npow(c, 3) + 33*npow(b, 2) *
        npow(c, 2) - 66*b*c*d) + 12*npow(b, 4)*c * (npow(d, 2) -
        7*npow(c, 3)) - npow(b, 2)*npow(c, 2)*d*(24*npow(b,3)+291*d) + npow(d,3)*(144*b*c - 2*npow(d, 3) - 27*d)

o = -4*npow(b, 3)*d + npow(b, 2)*npow(c, 2) + 18*b*c*d - 4*npow(c, 3) - 27*npow(d, 2)

d0 = 4*npow(b, 4)*npow(c, 2) - 4*npow(b, 3)*c*d - 14*npow(b, 2)*npow(c, 3) + npow(b, 2)*npow(d, 2) + 28*b*npow(c,2)*d + npow(c, 4) - 12*c*npow(d, 2)
print(t, o, d0)

b = Struct(init=b, deg2=npow(b,2), deg3=npow(b, 3))
c = Struct(init=c, deg2=npow(c, 2), deg3=npow(c, 3))
d = Struct(init=d, deg2=npow(d, 2))

r = (2*b.deg3 - 9*b()*c() + 27*d())/27
R1 = np.cbrt((sqrt2/9)*sqrt1 + r)
R2 = np.cbrt((sqrt2/9)*sqrt1 - r)

x1 = x2 = x3 = None

# METHOD 1
if o == 0 and r ==0:
    x1 = x2 = x3 = -b()/3
else:
    b.expand(deg4=npow(b(), 4), deg5=npow(b(), 5), deg6=npow(b(), 6))
    c.expand(deg4=npow(c(), 4))
    d.expand(deg3=npow(d(), 3))
    bl = (d()-b()*c()) * sqrt1 * (4*b.deg2*c.deg2 - 4*b()*c()*d() + 2*c.deg3 + d.deg2) + (sqrt2/9)*t
    A1 = (-2*sqrt2/3)*(4*b.deg3*c() - 2*d()*b.deg2 - 13*b()*c.deg2 + 15*d()*c()) + 2*c()*sqrt1
    A2 = 8*b.deg5*c.deg2 - 8*b.deg4*c()*d() - 40*b.deg3*c.deg3 + 2*b.deg3*d.deg2 + 116*b.deg2*c.deg2*d()
    A2 += 23*b()*c.deg4 - 99*b()*c()*d.deg2 - 21*c.deg3*d() + 27*d.deg3 - sqrt1*sqrt2 * (8*b.deg2*c.deg2 - 10*b()*c()*d() +
        c.deg3 + 3*d.deg2)

    print(bl, A1, A2)
print(x1, x2, x3)
