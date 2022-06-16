import time
import numpy as np
from MethodsArray import profile
from methods import fastpow as fpow

arr = np.random.randint(10, 100, (200, 1))

# @profile(strip_dirs=True)
def fpowtest(arr):
    return fpow(arr, 6)

# @profile(strip_dirs=True)
def nproottest(arr):
    np.power(arr, 6)

print("Тестируем скорость froot")
t = time.process_time_ns()
# result = fpowtest(arr)
resutl = np.apply_along_axis(fpowtest, 1, arr)
elapsed = time.process_time_ns() - t
print(f"Решено за {elapsed} наносекунд.")

print("Тестируем скорость np.power")
t = time.process_time_ns()
resutl = np.apply_along_axis(nproottest, 1, arr)
elapsed = time.process_time_ns() - t
print(f"Решено за {elapsed} наносекунд.")
