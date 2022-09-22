import time
import numpy as np
from MethodsArray import profile

arr = np.random.randint(10, 20, (10, 1))
arr = np.longlong(arr)
print("generated array", arr)
def fpowtest(arr):
    return fpow(arr, 10)

def fastpow(x, deg=10):
    """ Быстрое возведение в степень для натуральных чисел
    https://en.wikipedia.org/wiki/Exponentiation_by_squaring
    """
    if x == 1 or x == 0:
        return x
    if deg == 0:
        return 1
    if deg < 0:
        return 1 / power(x, -deg)
    ans = 1
    while deg:
        if deg & 1:
            ans *= x
        deg >>= 1
        x *= x
    return ans

def nproottest(arr):
    return np.power(arr, 10)

def fastbinpow(base):
    power = 10
    result = 1
    while power > 0:
        if power % 2 == 0:
            power = power // 2
            base = base * base
        else:
            power = power - 1
            result = result * base

            power = power // 2
            base = base * base

    return result

def BinaryPower(x, y=10):
    if y == 0:
        return 1
    tmp = np.power(x, y*0.5)
    if y % 2 == 0:
        return tmp * tmp
    else:
        return tmp * tmp * x


print("Тестируем скорость быстрого возведения в степень")
t = time.process_time_ns()
# result = fpowtest(arr)
result = np.apply_along_axis(fastpow, 1, np.copy(arr))
elapsed = time.process_time_ns() - t
print(result)
print(f"Решено за {elapsed} наносекунд.")

print("Тестируем скорость binary exponetiation")
t = time.process_time_ns()
# result = fpowtest(arr)
result = np.apply_along_axis(fastbinpow, 1, np.copy(arr))
elapsed = time.process_time_ns() - t
print(result)
print(f"Решено за {elapsed} наносекунд.")

print("Тестируем скорость бинарного возведения в степень")
t = time.process_time_ns()
# result = fpowtest(arr)
result = np.apply_along_axis(BinaryPower, 1, np.copy(arr))
elapsed = time.process_time_ns() - t
print(result)
print(f"Решено за {elapsed} наносекунд.")

print("Тестируем скорость np.power")
t = time.process_time_ns()
result = np.apply_along_axis(nproottest, 1, np.copy(arr))
elapsed = time.process_time_ns() - t
print(result)
print(f"Решено за {elapsed} наносекунд.")


