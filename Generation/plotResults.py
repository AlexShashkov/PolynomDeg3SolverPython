import matplotlib.pyplot as plt
from PIL import Image

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
                if res == False: falseres.append(value)
                else: trueres.append(value)
        line, = ax[cntr].plot(x, falseres, \
                label=f"{name}: wrong ans.")
        line, = ax[cntr].plot(x, trueres, \
                label=f"{name}: correct ans.")
        plt.ylabel("Корни")
        plt.xlabel("Шаг")
        ax[cntr].legend()
        cntr += 1
    plt.suptitle(title)
    return plt
    # with Image.open('testresults.png') as img:
        # img.show()

def plotTest(time, title, data):
    """
    График для одного теста
    """
    fig, ax = plt.subplots(len(data.keys()), 1)
    cntr = 0
    for name, results in data.items():
        ax[cntr].pie(results["count"], labels=results["unique"], autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax[cntr].axis('equal')
        ax[cntr].set_title(f"Результаты для {name}")
        cntr += 1
    plt.suptitle(title)
    return plt


