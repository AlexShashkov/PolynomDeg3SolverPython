import methods
from numpy import longdouble as ld, cbrt, longcomplex as lc
import numpy as np
import os
tolerance = lc(os.environ.get('tolerance', '1e-08'))
round_dec = bool(os.environ.get('roundto', 1))

inp = [lc(0)]*4
inp[3] = lc(input("Введите число при x³ > "))
inp[2] = lc(input("Введите число при x² > "))
inp[1] = lc(input("Введите число при x > "))
inp[0] = lc(input("Введите свободный член > "))

if inp[3]!=lc(1):
	item = inp[3].copy()
	inp = lc(list(map(lambda x: x/item, inp)))
print(inp)

Q = (inp[2]**lc(2) - 3*inp[1])/9
R = (2*inp[2]**3-9*inp[1]*inp[2]+27*inp[0])/54
S = Q**3 - R**2

print("Q, R, S", Q, R, S)
x1, x2, x3 = 0, 0, 0
if S>0:
    phi = np.arccos(R/np.sqrt(Q**3))/3
    x1 = -2*np.sqrt(Q)*np.cos(phi)-inp[2]/3
    x2 = 2*np.sqrt(Q)*np.cos(phi+2*np.pi/3)-inp[2]/3
    x3 = -2*np.sqrt(Q)*np.cos(phi-2*np.pi/3)-inp[2]/3
    print("Answer: x1", x1, " x2 ", x2, " x3 ", x3)
elif S < 0:
    phi = 0
    T = 0
    x2, x3 = 0, 0
    if Q>0:
        phi = methods.arch(np.abs(R)/np.sqrt(np.abs(Q**3)))/3
        T = np.sign(R)*np.sqrt(np.abs(Q))*methods.ch(phi)
        x2 = T - inp[2]/3+1j*np.sqrt(3)*np.sqrt(np.abs(Q))*methods.sh(phi)
        x3 = T - inp[2]/3-1j*np.sqrt(3)*np.sqrt(np.abs(Q))*methods.sh(phi)
    else:
        phi = methods.arsh(np.abs(R)/np.sqrt(np.abs(Q**3)))/3
        T = np.sign(R)*np.sqrt(np.abs(Q))*methods.sh(phi)
        x2 = T - inp[2]/3+1j*np.sqrt(3)*np.sqrt(np.abs(Q))*methods.ch(phi)
        x3 = T - inp[2]/3-1j*np.sqrt(3)*np.sqrt(np.abs(Q))*methods.ch(phi)
    x1 = -2*T-inp[2]/3
    print("Param phi", phi, "param T", T)
    print("Answer: x1", x1, " x2 ", x2, " x3 ", x3)
    print(type(x2), type( x3))

if np.isclose(0, S, tolerance):
    x1 = -ld(2)*cbrt(R)-inp[2]/ld(3)
    x2 = cbrt(R)-inp[2]/ld(3)
    print("Answer: x1", x1, "x2", x2)
