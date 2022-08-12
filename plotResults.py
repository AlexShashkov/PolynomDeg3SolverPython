import matplotlib.pyplot as plt

def plotSimpleTest(**kwargs):
    """
    График для нескольких тестов
    """
    fig, ax = plt.subplots()
    for name, results in kwargs.items():
        line, = ax.plot(results[0], results[1], label=f"${name}")
    ax.legend()
    plt.show()
