import time
import numpy as np
from MethodsArray import Array, profile
from methods import generateEquations
#import cProfile, pstats, io

@profile(strip_dirs=True)
def caller(solver, arr):
    return solver(arr)


def StartEquationsTest(**kwargs):
    inp = None
    while True:
        try:
            inp = input("Введите количество полиномов, которые будут сгенерированы. >")
            inp = int(inp)
        except Exception as ex:
            print("Ошибка. Попробуйте еще раз:", ex)
            continue
        break
    data = generateEquations(inp)
    coeffs = Array(data[0])
    answers = Array(data[1])

    for name, solver in kwargs.items():
        print(f"Тестируется метод {name}, кол-во уравнений: {inp}")
        # В наносекундах
        t = time.process_time_ns()
        result = caller(solver, coeffs)
        elapsed = time.process_time_ns() - t
        print(f"Решено за {elapsed} наносекунд.")
    a = input("vse")

# a = Baydoun(coeffs)
# b = Vieta(coeffs)
# 
# print(a)
# print(b)
