import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox

from Bezu import Bezu


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Bezu.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.run)
        self.cof0.setText('0')
        self.cof.setText('0')
        self.cof2.setText('0')
        self.cof3.setText('0')
        self.cof4.setText('0')

        self.result.setReadOnly(True)

    def isint(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def get_number(self, cof, n):
        if self.isint(cof) and len(cof) <= 5:
            return int(cof)
        else:
            QMessageBox.critical(self, "Ошибка ",
                                 f"Введены некорректные значения при {n}.\n(Строка или число больше 99999)",
                                 QMessageBox.Ok)
            return 0

    def run(self):
        cof0 = self.get_number(self.cof0.text(), 'x^0')
        cof1 = self.get_number(self.cof.text(), 'x')
        cof2 = self.get_number(self.cof2.text(), 'x^2')
        cof3 = self.get_number(self.cof3.text(), 'x^3')
        cof4 = self.get_number(self.cof4.text(), 'x^4')
        bezu = Bezu(cof4, cof3, cof2, cof1, cof0)
        self.result.setText(f'Результат решения уравнения {bezu} --- \n{bezu.result()}')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
