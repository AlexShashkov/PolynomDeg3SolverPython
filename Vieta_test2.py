"""
Пример одновременного нахождения корней для заданных уравнений:
    * x^3 -2x^2 -23x +60 = 0
    * x^3 + x^2 +X -3 = 0
    * X^3 -X^2 -21X + 45 = 0
"""

from numpy import longcomplex as lc
from Deg3Solvers.Vieta import Solver

solve = Solver()

inp = [
    [60, -23, -2, 1],
    [-3, 1, 1, 1],
    [45, -21, -1, 1]
]

print("Input matrix:", inp)
print(solve(inp))
