from consolemenu import *
from consolemenu.items import *
from numpy import longcomplex as lc

from Deg3Solvers.Baydoun import Solver as BSolver
from Deg3Solvers.Vieta import Solver as VSolver

from MethodsArray import Array

from Generation.methods import *
from Generation.GenerateEquations import *


menu = ConsoleMenu("PolynomDeg3Solver", "КМБО-03-20, 2022")
methods = {
    "Vieta": VSolver(),
    "Baydoun": BSolver()
}

def inp(method):
    print("Введите через пробел коэффициенты при c, x, x^2, x^3\n")
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
Testing_item2 = FunctionItem("Тестирование с комплексными корнями",
        StartEquationsTest, args=[generateComplexEquations], kwargs=methods)
Testing_item3 = FunctionItem("Тестирование с малыми комплексными корнями",
        StartEquationsMinValueTest, args=[generateIntegerEquations], kwargs=methods)
Testing_item4 = FunctionItem("Тестирование с малыми комплексными корнями (Exp)",
        StartEquationsMinExpValueTest, args=[generateExponentComplexEquations], kwargs=methods)

menu.append_item(Vieta_item)
menu.append_item(Baydoun_item)
menu.append_item(Testing_item2)
menu.append_item(Testing_item3)
# menu.append_item(Testing_item4)

menu.show()
