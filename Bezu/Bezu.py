from functools import singledispatch, update_wrapper
from math import exp

import numpy as np

NUN = exp(-20)


def methdispatch(func):
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


class Bezu:
    """для инициализации требуется 5 коэффициентов, тк по условию задачи мы ищем решение для многочленов
    не выше 4й степени. Также можно передавать сразу массив"""

    @methdispatch
    def __init__(self, a_0, a_1, a_2, a_3, a_4):
        self.coefficient = np.array([a_0, a_1, a_2, a_3, a_4])
        self.len_polynomial = self.coefficient.shape[0]
        self.roots = []

    @__init__.register(np.ndarray)
    def _(self, n, roots):
        self.coefficient = n
        self.roots = roots
        self.len_polynomial = self.coefficient.shape[0]

    def __str__(self):
        if self.coefficient.shape[0] == 5:
            return f'P(x) = {self.coefficient[0]}x\u2074 + {self.coefficient[1]}x\u00B3 +' \
                   f' {self.coefficient[2]}x\u00B2 + {self.coefficient[3]}x + {self.coefficient[4]}'
        elif self.coefficient.shape[0] == 4:
            return f'P(x) = {self.coefficient[0]}x\u00B3 +' \
                   f' {self.coefficient[1]}x\u00B2 + {self.coefficient[1]}x + {self.coefficient[3]}'
        elif self.coefficient.shape[0] == 3:
            return f'P(x) = {self.coefficient[0]}x\u00B2 + {self.coefficient[1]}x + {self.coefficient[2]}'
        elif self.coefficient.shape[0] == 2:
            return f'P(x) = {self.coefficient[0]}x + {self.coefficient[1]}'
        else:
            return f'P(x) = {self.coefficient[0]}'

    # данная функция возвращает один корень многочлена по результатам выполнения первых 4x пунктов(readme.md).
    def __root_polynomial(self):
        if np.sum(self.coefficient) == 0:
            return 1
        elif np.sum([self.coefficient[i] for i in range(self.len_polynomial) if i % 2 == 0]) == np.sum(
                [self.coefficient[i] for i in range(self.len_polynomial) if i % 2 != 0]):
            return -1
        else:
            divisors = self.__divisors(abs(self.coefficient[self.len_polynomial - 1]))
            root = self._decision(divisors)
            if root:
                return root
            else:
                if self.len_polynomial == 5:
                    return None
                elif self.len_polynomial == 3 or (self.coefficient[0] == 0 and self.len_polynomial == 4):
                    return 0
        # return None

    # Функция для нахождения делителей n
    def __divisors(self, n):
        result = set()
        for i in range(1, int(n ** 0.5) + 1):
            if n % i == 0:
                result.add(i)
                t = np.array([n]) // i
                result.add(t[0])
        return np.array(list(result))

    # Метод для проверки корня
    def _decision(self, n: np.ndarray):
        len_n = n.shape
        for i in range(len_n[0]):
            if self.__bezu(n[i]) == 0.0:
                return n[i]
            elif self.__bezu(-n[i]) == 0.0:
                return -n[i]
        return None

    def __bezu(self, parametr):
        result = 0
        for i in range(self.len_polynomial - 1):
            result += self.coefficient[i] * np.power(parametr, self.len_polynomial - i - 1)
        return result + self.coefficient[self.len_polynomial - 1]

    def result(self):
        per = self.__root_polynomial()
        # print(per)

        if per:
            self.roots.append(per)
            Bezu(np.polynomial.polynomial.polydiv(self.coefficient, (1, -per))[0], self.roots).result()
        elif per == 0:
            r = np.roots(self.coefficient)
            self.roots.append(r[0])
            self.roots.append(r[1])
            print(self.roots)
            # return self.roots
        else:
            if len(self.roots) > 0:
                print(self.roots)
                # return self.roots
            else:
                print('Нельзя воспользоваться методом Безу')