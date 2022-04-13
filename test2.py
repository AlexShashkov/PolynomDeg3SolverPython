from numpy import longcomplex as lc
from Vieta import Solver
inp = [lc(0)]*4

inp[3] = lc(input("Введите число при x³ > "))
inp[2] = lc(input("Введите число при x² > "))
inp[1] = lc(input("Введите число при x > "))
inp[0] = lc(input("Введите свободный член > "))

result = Solver(inp)()
print(result)

#print("One matrix method:")

#inp = [
#    [60, -23, -2, 1],
#    [-3, 1, 1, 1],
#    [45, -21, -1, 1]
#]

#print("Input matrix:", inp)
#print(Solver(inp)())
