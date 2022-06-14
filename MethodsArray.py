import time
from random import randint
from functools import singledispatch, update_wrapper, wraps
from types import SimpleNamespace
import numpy as np
from numpy import longcomplex as lc

import cProfile
import pstats

def profile(output_file=None, sort_by='cumulative', lines_to_print=None, strip_dirs=False):
    """Декоратор профайлера
    http://code.activestate.com/recipes/577817-profile-decorator/
    @type output_file: str
    @param output_file: Наименование файла для записи результата. По умолчанию
        будет записан в текущую папку с текущим временем.
    @type sort_by: str, tuple, list
    @param sort_by: По какому критерию будет происходить сортировка
            https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats
    @type lines_to_print: int
    @param lines_to_print: Количество строк вывода.
    @type strip_dirs: bool
    @returns: Профайлер для функции
    """

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ctm = time.localtime()
            ctm = time.strftime("%H%M%S", ctm)
            salt = str(randint(100, 999))
            _output_file = output_file or f"{func.__name__}{ctm}_{salt}.prof"
            pr = cProfile.Profile()
            pr.enable()
            retval = func(*args, **kwargs)
            pr.disable()
            pr.dump_stats(_output_file)

            with open(_output_file, 'w') as f:
                ps = pstats.Stats(pr, stream=f)
                if strip_dirs:
                    ps.strip_dirs()
                if isinstance(sort_by, (tuple, list)):
                    ps.sort_stats(*sort_by)
                else:
                    ps.sort_stats(sort_by)
                ps.print_stats(lines_to_print)
            return retval

        return wrapper

    return inner

def methdispatch(func):
    """ Декоратор для перегрузки функций.
    Для перегрузки после определения исходного метода необходимо использовать
    функцию register данного декоратора с типом, для которого необходимо выполнить
    перегрузку.
    """
    dispatcher = singledispatch(func)
    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


class Struct(SimpleNamespace):
    def __init__(self, **kwargs):
        """ Реализация структуры.
        @type kwargs: **kwargs
        @param kwargs: Именованные аргументы для хранения
        """
        super().__init__(**kwargs)
    def __call__(self):
        """ Быстрый доступ к необходимому элементу
        @returns: Элемент, указанный в аргументе init
        """
        return self.init
    def expand(self, **kwargs):
        """ Добавить новые переменные в структуру
        @type kwargs: **kwargs
        @param kwargs: Новые именованные аргументы для хранения
        """
        for key, value in kwargs.items():
            #print(key, value)
            #vars()[key] = value
            setattr(self, key, value)

class Array(object):
    # INIT
    @methdispatch
    def __init__(self, array):
        """Вспомогательная обертка для удобства. Поддерживает входные типы Numpy и обычные массивы. Хранящийся numpy массив возвращается с помощью вызова __call__.
        @type array: Array
        @param array: Необходимый для хранения массив
        """
        self.outputf = None
        self.values = array()
        if self.values.ndim == 1:
            self.values = self.values.reshape((1, self.values.shape[0]))
        self.shape = self.values.shape
    @__init__.register(list)
    def _(self, array):
        """ Переоперделение конструктора для list
        @type array: list
        @param array: Необходимый для хранения массив
        """
        self.outputf = None
        self.values = np.longcomplex(array)
        if self.values.ndim == 1:
           self.values = self.values.reshape((1, self.values.shape[0]))
        self.shape = self.values.shape
    @__init__.register(np.ndarray)
    def _(self, array):
        """ Переоперделение конструктора для numpy
        @type array: ndarray
        @param array: Необходимый для хранения массив
        """
        self.outputf = None
        self.values = array.copy()
        if self.values.ndim == 1:
            self.values = self.values.reshape((1, self.values.shape[0]))
        self.shape = self.values.shape

    # MISC
    def setOutputFunction(self, func):
        """ Установить собственную функцию вывода
        @type func: function
        @param func: Собственная функция для обработки вывода.
        """
        self.outputf = func

    def __call__(self) -> np.ndarray:
        """ Используется для получения хранящихся данных в виде numpy
        @rtype: ndarray
        @return: Необходимый для хранения массив
        """
        return self.values.copy()
    def __str__(self):
        """ Вывод
        @return: Вывод numpy массива или вывод из заданной функции.
        """
        if self.outputf is not None:
            return self.outputf(self)
        else:
            return f"Array:{self.shape}:\n{str(self.values.copy())}"
    def __getitem__(self, key):
        """ Получение элемента по ключу
        @rtype: Array
        @return: Строка по ключу key
        """
        return self.values[key]

    # +
    # Arrays
    @methdispatch
    def __add__(self, other):
        """ Поэлементное сложение двух объектов типа Array
        @rtype: Array
        @return: Новый Array
        """
        new_Array = Array(self.values)
        new_Array += other()
        return new_Array
    @__add__.register
    def _(self, other:list)  :
        other = Array(other)
        return self.__add__(other)
    @__add__.register
    def _(self, other:np.ndarray)  :
        other = Array(other)
        return self.__add__(other)
    # Numbers
    @__add__.register
    def _(self, other:np.longcomplex)  :
        new_Array = Array(self.values)
        new_Array += other
        return new_Array
    @__add__.register
    def _(self, other:float)  :
        other = np.longcomplex(other)
        return self.__add__(other)

    # +=
    # Arrays
    @methdispatch
    def __iadd__(self, other):
        """ Сложение со вторым объектом типа Array
        @rtype: Array
        @return: Измененный исходный объект
        """
        self.values += other()
        return self
    @__iadd__.register
    def _(self, other:list)  :
        other = Array(other)
        return self.__iadd__(other)
    @__iadd__.register
    def _(self, other:np.ndarray)  :
        other = Array(other)
        return self.__iadd__(other)
    @__iadd__.register
    # Numbers
    def _(self, other:np.longcomplex)  :
        self.values += other
        return self
    @__iadd__.register
    def _(self, other:float)  :
        other = np.longcomplex(other)
        return self.__iadd__(other)

    # *
    # Arrays
    @methdispatch
    def __mul__(self, other):
        """ Поэлементное умножение двух объектов типа Array
        @rtype: Array
        @return: Новый Array
        """
        new_Array = Array(self.values)
        new_Array *= other()
        return new_Array
    @__mul__.register
    def _(self, other:list) :
        other = Array(other)
        return self.__mul__(other)
    @__add__.register
    def _(self, other:np.ndarray):
        other = Array(other)
        return self.__mul__(other)
    # Numbers
    @__add__.register
    def _(self, other:np.longcomplex):
        new_Array = Array(self.values)
        new_Array *= other
        return new_Array
    @__add__.register
    def _(self, other:float):
        other = np.longcomplex(other)
        return self.__mul__(other)
    @__add__.register
    def _(self, other:int):
        other = np.longcomplex(other)
        return self.__mul__(other)
    @__add__.register
    def _(self, other:complex):
        other = np.longcomplex(other)
        return self.__mul__(other)

    # *=
    # Arrays
    @methdispatch
    def __imul__(self, other):
        """ Умножение со вторым объектом типа Array
        @rtype: Array
        @return: Измененный исходный объект
        """
        self.values = np.multiply(self.values, other.values)
        return self
    @__imul__.register
    def _(self, other:list) :
        other = Array(other)
        return self.__imul__(other)
    @__imul__.register
    def _(self, other:np.ndarray):
        other = Array(other)
        return self.__imul__(other)
    # Numbers
    @__imul__.register
    def _(self, other:np.longcomplex):
        self.values *= other
        return self
    @__imul__.register
    def _(self, other:float):
        self.values *= np.longcomplex(other)
        return self
    @__imul__.register
    def _(self, other:int):
        self.values *= np.longcomplex(other)
        return self
    @__imul__.register
    def _(self, other:complex):
        self.values *= np.longcomplex(other)
        return self
