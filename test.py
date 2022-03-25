from numpy import longdouble as ld, cbrt
import numpy as np
import os
tolerance =  ld(os.environ.get('tolerance', '1e-08'))

inp = [ld(0)]*4
inp[3] = ld(input("Введите число при x³ > "))
inp[2] = ld(input("Введите число при x² > "))
inp[1] = ld(input("Введите число при x > "))
inp[0] = ld(input("Введите свободный член > "))

if inp[3]!=ld(1):
	item = inp[3].copy()
	inp = list(map(lambda x: x/item, inp))
print(inp)

Q = (inp[2]**ld(2) - ld(3)*inp[1])/ld(9)
R = (ld(2)*inp[2]**ld(3)-ld(9)*inp[1]*inp[2]+ld(27)*inp[0])/ld(54)
S = Q**ld(3) - R**ld(2)

print(Q, R, S)

if S>0:
    pass
elif S < 0:
    pass
if np.isclose(0, S, tolerance):
    x1 = -ld(2)*cbrt(R)-inp[2]/ld(3)
    x2 = cbrt(R)-inp[2]/ld(3)
    print("Answer: x1", x1, "x2", x2)
