import argparse
from Deg3Solvers.Baydoun import Solver as BSolver
from Deg3Solvers.Vieta import Solver as VSolver
from Generation.GenerateEquations import *

from consolemenu import *
from consolemenu.items import *

def inp(method):
    print("Введите через пробел коэффициенты при c, x, x^2, x^3\n")
    got = input("> ")
    try:
        arr = np.fromstring(got, dtype=complex, sep=' ').reshape([1, 4])
        print(arr, arr.shape)
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
    "Complex": StartEquationsTest,
    "ComplexSmall": StartEquationsMinValueTest
}

parser = argparse.ArgumentParser(description="Демо для работы с методом Vieta и Baydoun")
parser.add_argument("-m", "--method", help="Запустить метод Vieta или Baydoun", default=None)
parser.add_argument("-t", "--test", help="Вид тестирования. Complex - сгенерировать корни. ComplexSmall - сгенерировать корни с шагом", default=None)
parser.add_argument("-si", "--saveinput", help="Нужно ли сохранить входные данные",action="store_true")
parser.add_argument("-c", "--count", help="Количество сгенерированных полиномов", default=100, type=int)
parser.add_argument("-s", "--saveresult", help="Нужно ли сохранить результаты", action="store_true")
parser.add_argument("-p", "--plot", help="Нужен ли график результатов", action="store_true")
parser.add_argument("-a", "--atol", help="Абсолютная погрешность", default=1e-08, type=float)
parser.add_argument("-r", "--rtol", help="Относительная погрещность", default=1e-05, type=float)
parser.add_argument("-mx", "--max", help="Максимальный множитель в тесте с малыми корнями", default=0.1, type=float)
parser.add_argument("-mn", "--min", help="Минимальный множитель в тесте с малыми корнями", default=0.001, type=float)
parser.add_argument("-st", "--step", help="Шаг для малых корней", default=0.005, type=float)

args = parser.parse_args()
print(args)

if args.method is None and args.test is None:
    menu = ConsoleMenu("PolynomDeg3Solver", "КМБО-03-20, 2022")
    Vieta_item = FunctionItem("Виета", inp, ["Vieta"])
    Baydoun_item = FunctionItem("Baydoun", inp, ["Baydoun"])
    Testing_item2 = FunctionItem("Тестирование с комплексными корнями",
            StartEquationsTest, args=[None], kwargs=methods)
    Testing_item3 = FunctionItem("Тестирование с малыми комплексными корнями",
            StartEquationsMinValueTest, args=[None], kwargs=methods)
    menu.append_item(Vieta_item)
    menu.append_item(Baydoun_item)
    menu.append_item(Testing_item2)
    menu.append_item(Testing_item3)
    menu .show()
elif args.method in methods.keys():
    inp(args.method)
tst = tests.get(args.test, None)
if tst is not None:
    tst(args, **methods)
