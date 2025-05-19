class Usuari:
    """
    Classe que representa un usuari de la biblioteca amb atributs bàsics.

    Atributs:
        nom (str): El nom de l'usuari. Per defecte és "None".
        cognoms (str): Els cognoms de l'usuari. Per defecte és "None".
        dni (str): El DNI de l'usuari. Per defecte és "None".

    Mètodes:
        __init__(nom="None", cognoms="None", dni="None"):
            Inicialitza una instància de la classe Usuari amb els atributs especificats.
        imprimir_dades():
            Retorna una cadena amb la informació de l'usuari.
        introduir_dades():
            Permet introduir les dades de l'usuari per consola.
    """

    def __init__(self, nom: str = "None", cognoms: str = "None", dni: str = "None"):
        self.nom = nom
        self.cognoms = cognoms
        self.dni = dni

    def imprimir_dades(self) -> str:
        return f"Nom: {self.nom}, Cognoms: {self.cognoms}, DNI: {self.dni}"

    def introduir_dades(self):
        self.nom = input("Introdueix el nom: ")
        self.cognoms = input("Introdueix els cognoms: ")
        self.dni = input("Introdueix el DNI: ")
