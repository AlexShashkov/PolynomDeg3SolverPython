import matplotlib.pyplot as plt
import time
import numpy as np
from MethodsArray import profile

arr = np.random.randint(10, 20, (100, 1))
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
    """
    Fast Power Algorithm - Exponentiation by Squaring
    https://www.rookieslab.com/posts/fast-power-algorithm-exponentiation-by-squaring-cpp-python-implementation
    """
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
    """
    Binary Exponentiation
    https://cp-algorithms.com/algebra/binary-exp.html#implementation
    """
    if y == 0:
        return 1
    tmp = np.power(x, y*0.5)
    if y % 2 == 0:
        return tmp * tmp
    else:
        return tmp * tmp * x

funcs = {
    "Exponentiation by squaring":{"eval": fastpow, "x":[], "y":[]},
    "Numpy power": {"eval": nproottest, "x":[], "y":[]},
    "Fast binary exponentiation": {"eval": fastbinpow, "x":[], "y":[]},
    "Binary exponentiation": {"eval": BinaryPower, "x":[], "y":[]}
}

for i in range(2, 20):
    for name, func in funcs.items():
        t = time.process_time_ns()
        result = np.apply_along_axis(func["eval"], 1, np.copy(arr))
        print(name, result)
        elapsed = time.process_time_ns() - t
        func["x"].append(i)
        func["y"].append(elapsed)

print(funcs)


for name, func in funcs.items():
    plt.plot(func["x"], func["y"], label=name)
plt.legend()
plt.ylabel("Наносекунды")
plt.xlabel("Степень")
plt.savefig(f"fastpow-test.png")
