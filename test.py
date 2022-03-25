import methods
from numpy import longdouble as ld, cbrt
import numpy as np
import os
tolerance = ld(os.environ.get('tolerance', '1e-08'))
round_dec = bool(os.environ.get('roundto', 1))

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

print("Q, R, S", Q, R, S)
x1, x2, x3 = 0, 0, 0
if S>0:
    phi = np.arccos(R/np.sqrt(Q**ld(3)))/ld(3)
    x1 = -ld(2)*np.sqrt(Q)*np.cos(phi)-inp[2]/ld(3)
    x2 = -ld(2)*np.sqrt(Q)*np.cos(phi+ld(2)*np.pi/ld(3))-inp[2]/ld(3)
    x3 = -ld(2)*np.sqrt(Q)*np.cos(phi-ld(2)*np.pi/ld(3))-inp[2]/ld(3)
    print("Answer: x1", x1, " x2 ", x2, " x3 ", x3)
elif S < 0:
    phi = 0
    T = 0
    x2, x3 = 0, 0
    if Q>0:
        phi = methods.arch(R/np.sqrt(np.abs(Q**ld(3))))/ld(3)
        T = np.sign(R)*np.sqrt(np.abs(Q))*methods.ch(phi)
        x2 = T - inp[2]/ld(3) # TODO: COMPLEX NUMBERS
    else:
        phi = methods.arsh(R/np.sqrt(np.abs(Q**ld(3))))/ld(3)
        T = np.sign(R)*np.sqrt(np.abs(Q))*methods.sh(phi)
    x1 = -ld(2)*T-inp[2]/ld(3)

if np.isclose(0, S, tolerance):
    x1 = -ld(2)*cbrt(R)-inp[2]/ld(3)
    x2 = cbrt(R)-inp[2]/ld(3)
    print("Answer: x1", x1, "x2", x2)
