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
        ax[cntr].legend()
        cntr += 1
    plt.suptitle(title)
    return plt
    # with Image.open('testresults.png') as img:
        # img.show()
