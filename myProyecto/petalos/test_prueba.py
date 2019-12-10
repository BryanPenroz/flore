import unittest
from prueba import probar

class testPrueba(unittest:testCase):
    def test_suma(self):
        self.assertAlmostEqual(probar(3,5),8)
        self.assertAlmostEqual(probar(3,0),3)
        self.assertAlmostEqual(probar(3,1),4)