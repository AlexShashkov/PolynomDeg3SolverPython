from Deg3Solvers import Vieta, Baydoun
import numpy as np

Vieta = Vieta.Solver()
Baydoun = Baydoun.Solver()

arr = np.array([1, 2, 3, 4], dtype=np.float64)
print(Vieta(arr))
print(Baydoun(arr))
