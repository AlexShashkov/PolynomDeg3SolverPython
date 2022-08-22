import time
from datetime import datetime
import numpy as np
from MethodsArray import Array, profile
from Generation.plotResults import *

def test(solver, coeffs, answers, rtol) -> list:
    t = time.process_time_ns()
    result = solver(coeffs)
    elapsed = time.process_time_ns() - t
    _result = np.sort(result())
    _answers = np.sort(answers())
    # print("Получено:", _result)
    # print("Ожидалось:", _answers)
    _result = np.isclose(_result, _answers, rtol=rtol)
    # print(_result)
    unique, counts = np.unique(_result, return_counts=True)

    return (elapsed, unique, counts)

def StartEquationsTest(generator, **kwargs) -> None:
    start = str(datetime.now())
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
    # print("Сгенерированные полиномы:\n", coeffs)
    # print("Сгенерированные ответы:\n", answers)
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
    start = str(datetime.now())
    inp    = None
    rtol   = None
    maxVal = None
    minVal = None
    step   = None
    while True:
        try:
            inp = input("Введите количество полиномов, которые будут сгенерированы. >")
            inp = int(inp)
            rtol = input("Введите допустимую погршеность. >")
            rtol = int(inp)
            maxVal = input("Введите максимальный разряд. >")
            maxVal = float(maxVal)
            minVal = input("Введите минимальный разряд. >")
            minVal = float(minVal)
            step = input("Введите шаг. >")
            step = float(step)
            if minVal > maxVal: raise("Минимальное значение не может быть больше \
                    максимального!")
        except Exception as ex:
            print("Ошибка. Попробуйте еще раз:", ex)
            continue
        break

    res = {}
    for name, _ in kwargs.items():
        res[name] = []

    print(f"Начинаю тестирование разрядов от {maxVal} до {minVal}")
    for i in np.arange(minVal, maxVal, step)[::-1]:
        print(f"Разряд {i}")

        data = generator(inp, 10, 0)
        coeffs = Array(data[0]*i)
        answers = Array(data[1]*i)
        # print("Сгенерированные полиномы:\n", coeffs)
        # print("Сгенерированные ответы:\n", answers)


        for name, solver in kwargs.items():
            print(f"Тестируется метод {name}, кол-во уравнений: {inp}")
            elapsed, unique, count = test(solver, coeffs, answers, rtol)
            # print(f"Решено за {elapsed} тактов.")
            # print(unique.shape)
            results = dict(zip(unique, count))
            if False not in results.keys(): results[False]=0
            if True not in results.keys(): results[True]=0
            # print(results)
            test_result = {
                "step":i,
                "time":elapsed,
                "result":results,
            }
            res[name].append(test_result)
        # print(res)
    plt = plotTest(start, f"Проверка минимальных значений от {minVal} до {maxVal}", res)
    plt.savefig(f"many-{rtol}-{step}-{time}.png")
    _ = input("Готово. Нажмите любую кнопку чтобы вернуться в меню.")

def StartEquationsMinExpValueTest(generator, **kwargs) -> None:
    # TODO: другая метрика для очень маленьких значений?
    start = str(datetime.now())
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

    res = {}
    for name, _ in kwargs.items():
        res[name] = []

    print(f"Начинаю тестирование экспонент от {maxVal} до {minVal}")
    for i in range(maxVal, minVal, -1):
        print(f"Минимальная проверка значений экспоненты {i}")

        data = generator(inp, i, i-1)
        coeffs = Array(data[0])
        answers = Array(data[1])
        # print("Сгенерированные полиномы:\n", coeffs)
        # print("Сгенерированные ответы:\n", answers)


        for name, solver in kwargs.items():
            print(f"Тестируется метод {name}, кол-во уравнений: {inp}")
            elapsed, unique, count = test(solver, coeffs, answers, rtol)
            # print(f"Решено за {elapsed} тактов.")
            print(unique.shape)
            results = dict(zip(unique, count))
            if False not in results.keys(): results[False]=0
            if True not in results.keys(): results[True]=0
            # print(results)
            test_result = {
                "step":i,
                "time":elapsed,
                "result":results,
            }
            res[name].append(test_result)
        # print(res)
    plt = plotTest(start, f"Проверка минимальных значений, exp в степени [{maxVal},{minVal}].", res)
    plt.savefig(f"many-{rtol}-{step}-{time}.png")
    _ = input("Готово. Нажмите любую кнопку чтобы вернуться в меню.")
