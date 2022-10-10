import time
import numpy as np
import json
from Generation.plotResults import *
from Generation.methods import *

def test(solver, coeffs, answers, rtol, atol) -> list:
    """
    Запускает тестирование метода
    @type solver: Solver
    @param solver: Объект метода решения полиномов.
    @rtype: list
    @returns: Вернет лист со временем решения, видами ответов, количество
    ответов, полученный результат и ожидаемый
    """
    t = time.process_time_ns()
    result = solver(coeffs)
    elapsed = time.process_time_ns() - t
    _result = np.sort(result)
    # для тестирования отсортируем корни, сравним
    # каждый с каждым
    _answers = np.sort(answers)
    _res = np.isclose(_result, _answers, rtol=rtol, atol=atol)
    unique, counts = np.unique(_res, return_counts=True)

    return (elapsed, unique, counts, _result, _answers)
def StartEquationsTest(params, **kwargs) -> None:
    """
    Тестирование с обычными комплексными корнями
    @type params: dir
    @param params: Список аргументов, с которыми программа была запущена
    @type **kwargs: kwargs
    @param: именованный список с генератором корней и методами для
    решения уравнений
    """
    generator = generateComplexEquations
    start = str(time.time())
    inp, rtol, atol = None, None, None
    saveInput, saveResults = False, False
    savePlot = True

    if params is None:
        while True:
            try:
                inp = input("Введите количество полиномов, которые будут сгенерированы. >")
                inp = int(inp)
                rtol = input("Введите относительную погршеность. >")
                rtol = float(rtol)
                atol = input("Введите абсолютную погршеность. >")
                atol = float(atol)
            except Exception as ex:
                print("Ошибка. Попробуйте еще раз:", ex)
                continue
            break
    else:
        inp=params.count
        rtol=params.rtol
        atol=params.atol
        saveInput=params.saveinput
        saveResults=params.saveresult
        savePlot=params.plot
    # Генерируем коэффициенты полиномов и корни
    data = generator(inp)
    coeffs, answers = data[0], data[1]
    if saveInput:
        # Сохраняем коэффициенты и корни в файл
        np.savetxt(f"test-input-{start}.txt", coeffs)
        np.savetxt(f"test-original-{start}.txt", answers)
    res = {}

    for name, solver in kwargs.items():
        print(f"Тестируется метод {name}, кол-во уравнений: {inp}")
        test_result = None
        try:
            elapsed, unique, count, _res, _answ = test(solver, coeffs, answers, rtol, atol)
            if saveResults:
                # Сохраняем полученный результат в файле
                # test-result-{название метода}-{начало тестирования}.txt
                np.savetxt(f"test-result-{name}-{start}.txt", _res)
            print(f"Решено за {elapsed} наносекунд.")
            test_result = {
                "time":elapsed,     # время исполнения
                "res":len(unique),  # количество всех корней
                "unique":unique,    # True или False
                "count":count       # И количество правильных/неправильных
            }
        except Exception as ex:
            test_result = {
                "time":0,
                "res":0,
                "unique":0,
                "count":0
            }
            print("Что-то пошло не так.", ex)
        res[name] = test_result

    print(res)

    if savePlot:
        # Рисуем и сохраняем график
        plt = pieTest(start,
           f"Тестирование {inp} полиномов. atol - {atol}, rtol - {rtol}.",
           res
        )
        plt.savefig(f"test-{rtol}-{atol}-{start}.png")
    if params is None:
        _ = input("Готово. Нажмите любую кнопку чтобы вернуться в меню.")

def StartEquationsMinValueTest(params, **kwargs) -> None:
    """
    Тестирование с генерацией убывающих корней
    @type params: dir
    @param params: Список аргументов, с которыми программа была запущена
    @type **kwargs: kwargs
    @param: именованный список с генератором корней и методами для
    решения уравнений
    """
    generator = generateIntegerEquations
    start = str(time.time())

    inp, rtol, atol = None, None, None
    saveInput, saveResults, savePlot = False, False, True
    maxVal, minVal, step = None, None, None
    if params is None:
        while True:
            try:
                inp = input("Введите количество полиномов, которые будут сгенерированы. >")
                inp = int(inp)
                rtol = input("Введите относительную погршеность. >")
                rtol = float(rtol)
                atol = input("Введите абсолютную погршеность. >")
                atol = float(atol)
                maxVal = input("Введите максимальный разряд. >")
                maxVal = float(maxVal)
                minVal = input("Введите минимальный разряд. >")
                minVal = float(minVal)
                step = input("Введите шаг. >")
                step = float(step)
                if minVal > maxVal: raise Exception("Минимальное значение не может быть больше максимального!")
            except Exception as ex:
                print("Ошибка. Попробуйте еще раз:", ex)
                continue
            break
    else:
        inp=params.count
        rtol=params.rtol
        atol=params.atol
        maxVal = params.max
        minVal = params.min
        step = params.step
        saveInput=params.saveinput
        saveResults=params.saveresult
        savePlot=params.plot

    res = {}
    for name, _ in kwargs.items():
        res[name] = []

    print(f"Начинаю тестирование разрядов от {maxVal} до {minVal}, atol \
        {atol}, rtol {rtol}")
    for i in np.arange(minVal, maxVal, step)[::-1]:
        # Для каждого шага корня от большего к меньшему
        print(f"Разряд {i}")

        data = generator(inp, coeff=i)
        coeffs, answers = data[0], data[1]
        print("Сгенерированные полиномы:\n", coeffs)
        print("Сгенерированные ответы:\n", answers)
        if saveInput:
            np.savetxt(f"input-{i}-{start}.txt", coeffs)
            np.savetxt(f"original-{i}-{start}.txt", answers)

        for name, solver in kwargs.items():
            print(f"Тестируется метод {name}, кол-во уравнений: {inp}")
            test_result = None
            try:
                elapsed, unique, count, _res, _answ = test(solver, coeffs, answers, rtol, atol)
                print(f"Решено за {elapsed} наносекунд.")
                if saveResults:
                    # Сохраняем полученный результат в файле
                    # test-result-{название метода}-{начало тестирования}.txt
                    np.savetxt(f"result-{name}-{i}-{start}.txt", _res)
                results = dict(zip(unique, count))
                if False not in results.keys(): results[False]=0
                if True not in results.keys(): results[True]=0
                test_result = {
                    "step":i,           # текущий шаг корня
                    "time":elapsed,     # время исполнения
                    "result":results,   # True или False
                }
            except Exception as ex:
                print("Что-то пошло не так.", ex)
                test_result = {
                    "step":i,
                    "time":0,
                    "result":{
                        True: 0,
                        False: inp*3
                    },
                }

            res[name].append(test_result)
    if savePlot:
        # Рисуем график
        plt = plotTest(start,
           f"Проверка минимальных комплексных значений от {minVal} до {maxVal}. \natol - {atol}, rtol - {rtol}. Шаг - {step}",
           res
        )
        plt.savefig(f"many-{rtol}-{step}-{start}.png")
    if params is None:
        _ = input("Готово. Нажмите любую кнопку чтобы вернуться в меню.")
