#Файл только для тестирования и в конечный проект не входит
#Сделан, чтобы грустному воробушку зачли работу в крутой комманде 3ей группы

import unittest
from Bezu import Bezu

class TestBezu(unittest.TestCase):
    def setUp(self):
        self.bezu = Bezu(0,0,0,0,0)
    def testData(self):
        self.assertEqual(self.bezu.result(), "Бесконечно много решений")
    def testData2(self):
        self.bezu = Bezu(1,2,3,4,5)
        self.assertEqual(self.bezu.result(), "Нельзя воспользоваться методом Безу")
    def testData3(self):
        self.bezu = Bezu(5,3,2,5,1)
        self.assertEqual(self.bezu.result(), [-1]) #Если сумма коэффициентов многочлена  при четных степенях
                                                   # равна сумме коэффициентов при нечетных степенях, то число -1
                                                   #является корнем многочлена
    def testData4(self):
        self.bezu = Bezu(0,2,-3,5,-14)
        self.assertEqual(self.bezu.result(), [2, (-0.25+1.8540496217739157j), (-0.25-1.8540496217739157j)])
    def testData5(self):
        self.bezu = Bezu(10,-10,-15,15,0)
        self.assertEqual(self.bezu.result(), [1, 1.224744871391589, -1.2247448713915892]) #вроде как тут ещё корень 0 подходит
                                                                                          #но я хз - а можем мы его показывать или нет
    def testData6(self):
        self.bezu = Bezu(-0.249999999999999945, -0.249999999999999946, -0.249999999999999947, -0.249999999999999948, 0)
        self.assertEqual(self.bezu.result(), [-1, 1j, -1j])

if __name__ == "__main__":
    unittest.main()
