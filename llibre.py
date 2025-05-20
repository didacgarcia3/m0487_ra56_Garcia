class Llibre:
    """
    Classe que representa un llibre d'una biblioteca.

    Atributs:
        titol (str): El títol del llibre. Per defecte és "None".
        autor (str): L'autor del llibre. Per defecte és "None".
        dni_prestec (str): El DNI de l'usuari que té el llibre en préstec, o "None" si està disponible.

    Mètodes:
        __init__(titol="None", autor="None", dni_prestec="None"):
            Inicialitza una instància de Llibre amb els atributs indicats.
        imprimir_dades():
            Retorna una cadena amb la informació del llibre i estat del préstec.
        introduir_dades():
            Permet introduir les dades del llibre per consola.
    """

    def __init__(self, titol: str = "None", autor: str = "None", dni_prestec: str = "None"):
        self.titol = titol
        self.autor = autor
        self.dni_prestec = dni_prestec

    def imprimir_dades(self) -> str:
        if self.dni_prestec == "None":
            estat = "Disponible"
        else:
            estat = f"Prestat a {self.dni_prestec}"
        return f"Títol: {self.titol}, Autor: {self.autor}, Estat: {estat}"

    def introduir_dades(self):
        self.titol = input("Introdueix el títol del llibre: ")
        self.autor = input("Introdueix l'autor del llibre: ")
        self.dni_prestec = "None"
