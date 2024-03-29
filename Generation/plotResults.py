from PIL import Image
import matplotlib.pyplot as plt

def plotTest(time, title, data):
    """
    График для нескольких тестов
    """
    fig, ax = plt.subplots(len(data.keys()), 1)
    cntr = 0
    for name, results in data.items():
        x = [item["step"] for item in results]
        falseres = []
        trueres = []
        for got in results:
            for res, value in got["result"].items():
                # Отсеим True и False в отдельные массивы
                if res == False: falseres.append(value)
                else: trueres.append(value)
        line, = ax[cntr].plot(x, falseres, \
                label=f"{name}: wrong ans.")
        line, = ax[cntr].plot(x, trueres, \
                label=f"{name}: correct ans.")
        plt.ylabel("Корни")
        plt.xlabel("Шаг")
        ax[cntr].legend()
        # Счетчик показывает, какой график метода сейчас рисуется
        cntr += 1
    plt.suptitle(title)
    return plt
    # with Image.open('testresults.png') as img:
        # img.show()

def pieTest(time, title, data):
    """
    График для одного теста
    """
    fig, ax = plt.subplots(len(data.keys()), 1)
    cntr = 0
    for name, results in data.items():
        # Для каждого метода и его результатов
        ax[cntr].pie(results["count"], labels=results["unique"], autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax[cntr].axis('equal')
        ax[cntr].set_title(f"Результаты для {name}")
        # Счетчик показывает, какой график метода сейчас рисуется
        cntr += 1
    plt.suptitle(title)
    return plt


