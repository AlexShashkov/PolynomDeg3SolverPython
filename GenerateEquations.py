import numpy as np
from Deg3Solvers.Baydoun import Solver as BSolver
from Deg3Solvers.Vieta import Solver as VSolver
from MethodsArray import Array
from methods import generateEquations
#import cProfile, pstats, io

#pr = cProfile.Profile()
Baydoun = BSolver()
Vieta = VSolver()

data = generateEquations()
coeffs = Array(data[0])
answers = Array(data[0])

a = Baydoun(coeffs)
b = Vieta(coeffs)

print(a)
print(b)
