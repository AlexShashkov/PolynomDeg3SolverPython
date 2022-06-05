from consolemenu import *
from consolemenu.items import *
from numpy import longcomplex as lc
from Deg3Solvers.Baydoun import Solver as BSolver
from Deg3Solvers.Vieta import Solver as VSolver
from MethodsArray import Array


menu = ConsoleMenu("PolynomDeg3Solver", "КМБО, 2022")
methods = {
    "vieta": VSolver(),
    "bayd": BSolver()
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

# A FunctionItem runs a Python function when selected
Vieta_item = FunctionItem("Виета", inp, ["vieta"])
Baydoun_item = FunctionItem("Baydoun", inp, ["bayd"])


selection_menu = SelectionMenu(["item1", "item2", "item3"])
submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

menu.append_item(Vieta_item)
menu.append_item(Baydoun_item)

menu.show()
