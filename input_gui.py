from consolemenu import *
from consolemenu.items import *
from numpy import longcomplex as lc
from Deg3Solvers.Baydoun import Solver as BSolver
from Deg3Solvers.Vieta import Solver as VSolver
from MethodsArray import Array

from GenerateEquations import StartEquationsTest


menu = ConsoleMenu("PolynomDeg3Solver", "КМБО-03-20, 2022")
methods = {
    "Vieta": VSolver(),
    "Baydoun": BSolver()
}

def inp(method):
    print("Введите через пробел коэффициенты при x^3, x^2, x и c\n")
    got = input("> ")
    try:
        arr = Array(got.split())
        arr = methods[method](arr)
        print("Ответ: ", arr)
        input()
    except Exception as ex:
        print(f"Коэффициенты введены неверно. {ex}")
        input()

Vieta_item = FunctionItem("Виета", inp, ["Vieta"])
Baydoun_item = FunctionItem("Baydoun", inp, ["Baydoun"])
Testing_item = FunctionItem("Тестирование", StartEquationsTest, kwargs=methods)


menu.append_item(Vieta_item)
menu.append_item(Baydoun_item)
menu.append_item(Testing_item)

menu.show()
