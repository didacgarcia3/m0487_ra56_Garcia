import unittest
from datetime import date

# Suposem que la classe Llibre està definida així:
class Llibre:
    def __init__(self, titol, autor):
        self.titol = titol
        self.autor = autor
        self.dni_prestec = None
        self.data_prestec = None

    def prestar(self, dni):
        if self.dni_prestec is None:
            self.dni_prestec = dni
            self.data_prestec = date.today()
            return True
        return False

    def tornar(self):
        if self.dni_prestec is not None:
            self.dni_prestec = None
            self.data_prestec = None
            return True
        return False

class TestLlibre(unittest.TestCase):
    def setUp(self):
        self.llibre = Llibre("1984", "George Orwell")

    def test_creacio_llibre(self):
        self.assertEqual(self.llibre.titol, "1984")
        self.assertEqual(self.llibre.autor, "George Orwell")
        self.assertIsNone(self.llibre.dni_prestec)
        self.assertIsNone(self.llibre.data_prestec)

    def test_prestec_llibre(self):
        resultat = self.llibre.prestar("12345678A")
        self.assertTrue(resultat)
        self.assertEqual(self.llibre.dni_prestec, "12345678A")
        self.assertEqual(self.llibre.data_prestec, date.today())

    def test_prestec_llibre_ja_prestat(self):
        self.llibre.prestar("12345678A")
        resultat = self.llibre.prestar("87654321B")
        self.assertFalse(resultat)
        self.assertEqual(self.llibre.dni_prestec, "12345678A")  # Ha de mantenir-se

    def test_tornar_llibre(self):
        self.llibre.prestar("12345678A")
        resultat = self.llibre.tornar()
        self.assertTrue(resultat)
        self.assertIsNone(self.llibre.dni_prestec)
        self.assertIsNone(self.llibre.data_prestec)

    def test_tornar_llibre_no_prestat(self):
        resultat = self.llibre.tornar()
        self.assertFalse(resultat)

if __name__ == '__main__':
    unittest.main()