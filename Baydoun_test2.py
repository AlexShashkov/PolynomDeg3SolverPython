from numpy import longcomplex as lc
from Deg3Solvers.Baydoun import Solver

solve = Solver()

inp = [
    [-294, -35, 8, 1],
    [-220864, 11000, -182, 1],
    [17173512, -66564, -258, 1],
]

print("Input matrix:", inp)
print(solve(inp))
