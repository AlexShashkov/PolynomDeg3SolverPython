import time
import numpy as np
from MethodsArray import Array, profile
from plotResults import *
#import cProfile, pstats, io

def test(solver, coeffs, answers, rtol) -> list:
        t = time.process_time_ns()
        result = solver(coeffs)
        elapsed = time.process_time_ns() - t
        _result = np.sort(result())
        _answers = np.sort(answers())
        print("Получено:", _result)
        print("Ожидалось:", _answers)
        _result = np.isclose(_answers, _result, rtol=rtol)
        # print(_result)
        unique, counts = np.unique(_result, return_counts=True)
        # print("Unique n counts")
        # print(unique)
        # print(counts)

        return (elapsed, unique, counts)

def StartEquationsTest(generator, **kwargs) -> None:
    inp = None
    rtol = None
    while True:
        try:
            inp = input("Введите количество полиномов, которые будут сгенерированы. >")
            inp = int(inp)
            rtol = input("Введите допустимую погршеность. >")
            rtol = int(inp)
        except Exception as ex:
            print("Ошибка. Попробуйте еще раз:", ex)
            continue
        break
    data = generator(inp)
    coeffs = Array(data[0])
    answers = Array(data[1])
    print("Сгенерированные полиномы:\n", coeffs)
    print("Сгенерированные ответы:\n", answers)
    res = {}


    for name, solver in kwargs.items():
        print(f"Тестируется метод {name}, кол-во уравнений: {inp}")
        elapsed, unique, count = test(solver, coeffs, answers, rtol)
        print(f"Решено за {elapsed} тактов.")
        test_result = {
                "time":elapsed,
                "res":len(unique),
                "unique":unique,
                "count":count
        }
        res[name] = test_result

    print(res)
    _ = input("Готово. Нажмите любую кнопку чтобы вернуться в меню.")


def StartEquationsMinValueTest(generator, **kwargs) -> None:
    inp = None
    rtol = None
    maxVal = None
    minVal = None
    while True:
        try:
            inp = input("Введите количество полиномов, которые будут сгенерированы. >")
            inp = int(inp)
            rtol = input("Введите допустимую погршеность. >")
            rtol = int(inp)
            maxVal = input("Введите максимально возможную степень экспоненты. >")
            maxVal = int(maxVal)
            minVal = input("Введите минимально возможную степень экспоненты. >")
            minVal = int(minVal)
            if minVal > maxVal: raise("Минимальное значение не может быть больше \
                    максимального!")
        except Exception as ex:
            print("Ошибка. Попробуйте еще раз:", ex)
            continue
        break
    print(f"Начинаю тестирование экспонент от {maxVal} до {minVal}")
    for i in range(maxVal, minVal, -1):
        print(f"Минимальная проверка значений экспоненты {i}")

        data = generator(inp, i, i-1)
        coeffs = Array(data[0])
        answers = Array(data[1])
        print("Сгенерированные полиномы:\n", coeffs)
        print("Сгенерированные ответы:\n", answers)
        res = {}


        for name, solver in kwargs.items():
            print(f"Тестируется метод {name}, кол-во уравнений: {inp}")
            elapsed, unique, count = test(solver, coeffs, answers, rtol)
            print(f"Решено за {elapsed} тактов.")
            test_result = {
                    "time":elapsed,
                    "res":len(unique),
                    "unique":unique,
                    "count":count
            }
            res[name] = test_result
        print(res)
    _ = input("Готово. Нажмите любую кнопку чтобы вернуться в меню.")
