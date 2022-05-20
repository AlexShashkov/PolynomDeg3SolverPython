from types import SimpleNamespace as struct

import methods
from numpy import longdouble as ld, cbrt, longcomplex as lc, power as npow
import numpy as np

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

b = struct(self=b, square=npow(b,2), cube=npow(b, 3))
c= struct(self=c, square=npow(c, 2), cube=npow(c, 3))
d = struct(self=d, square=npow(d, 2))

print(b, c, d.self)

r = (2*b.cube - 9*b.self*c.self + 27*d.self)/27

x1 = x2 = x3 = None
if o == 0 and r ==0:
    x1 = x2 = x3 = -b.self/3
print(x1, x2, x3)
