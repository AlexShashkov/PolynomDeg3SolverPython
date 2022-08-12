import time
import numpy as np
from MethodsArray import profile
from methods import fastpow as fpow

arr = np.random.randint(10, 100, (200, 1))
print("generated array", arr)
# @profile(strip_dirs=True)
def fpowtest(arr):
    return fpow(arr, 10)

# @profile(strip_dirs=True)
def nproottest(arr):
    return np.power(arr, 10)

def fastbinpow(base):
    power = 10
    result = 1
    while power > 0:
        # If power is even
        if power % 2 == 0:
            # Divide the power by 2
            power = power // 2
            # Multiply base to itself
            base = base * base
        else:
            # Decrement the power by 1 and make it even
            power = power - 1
            # Take care of the extra value that we took out
            # We will store it directly in result
            result = result * base

            # Now power is even, so we can follow our previous procedure
            power = power // 2
            base = base * base

    return result

def _pow3(x, y=10):
    if y == 0:
        return 1
    if y == -1:
        return 1. / x
    p = _pow3(x, y // 2)
    p *= p
    if y % 2:
        p *= x
    return p

print("Тестируем скорость fpow")
t = time.process_time_ns()
# result = fpowtest(arr)
result = np.apply_along_axis(fpowtest, 1, np.copy(arr))
elapsed = time.process_time_ns() - t
#print(result) 
print(f"Решено за {elapsed} наносекунд.")


print("Тестируем скорость fpow2")
t = time.process_time_ns()
# result = fpowtest(arr)
result = np.apply_along_axis(_pow3, 1, np.copy(arr))
elapsed = time.process_time_ns() - t
#print(result)
print(f"Решено за {elapsed} наносекунд.")

print("Тестируем скорость binary exponetiation")
t = time.process_time_ns()
# result = fpowtest(arr)
result = np.apply_along_axis(fastbinpow, 1, np.copy(arr))
elapsed = time.process_time_ns() - t
#print(result)
print(f"Решено за {elapsed} наносекунд.")


print("Тестируем скорость np.power")
t = time.process_time_ns()
result = np.apply_along_axis(nproottest, 1, np.copy(arr))
elapsed = time.process_time_ns() - t
#print(result)
print(f"Решено за {elapsed} наносекунд.")
