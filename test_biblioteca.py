import unittest
from usuari import Usuari
from biblioteca import Biblioteca

class TestUsuari(unittest.TestCase):
    def test_creacio_usuari(self):
        u = Usuari("Anna", "Martínez", "12345678A")
        self.assertEqual(u.nom, "Anna")
        self.assertEqual(u.dni, "12345678A")



if __name__ == '__main__':
    unittest.main()