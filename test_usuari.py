import unittest
from usuari import Usuari

class TestUsuari(unittest.TestCase):
    def test_creacio_usuari(self):
        usuari = Usuari("Marc", "Pérez", "12345678A")
        self.assertEqual(usuari.nom, "Marc")
        self.assertEqual(usuari.cognoms, "Pérez")
        self.assertEqual(usuari.dni, "12345678A")



if __name__ == '__main__':
    unittest.main()