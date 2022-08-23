import argparse
from Deg3Solvers.Baydoun import Solver as BSolver
from Deg3Solvers.Vieta import Solver as VSolver
from MethodsArray import Array
from Generation.methods import *
from Generation.GenerateEquations import *

from consolemenu import *
from consolemenu.items import *

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

methods = {
    "Vieta": VSolver(),
    "Baydoun": BSolver()
}

tests = {
    "Complex": None,
    "ComplexSmall": None
}

parser = argparse.ArgumentParser(description="App for solving and testing \
    Vieta/Baydoun methods ")
parser.add_argument("-m", "--method", help="Launches Vieta OR Baydoun method",\
        default=None)
parser.add_argument("-t", "--test", \
        help="Run test:1 for random complex numbers, 2 for small random \
        complex numbers", default=None)
parser.add_argument("-si", "--saveinput", help="Saves initial input",\
        action="store_true")
parser.add_argument("-s", "--saveresult", help="Saves results", action="store_true")
parser.add_argument("-p", "--plot", help="Plot test results", action="store_true")

args = parser.parse_args()
print(args)

if args.method is None and args.test is None:
    menu = ConsoleMenu("PolynomDeg3Solver", "КМБО-03-20, 2022")
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
elif args.method in methods.keys():
    inp(args.method)
elif args.test in tests.keys(): print("Amog us")
