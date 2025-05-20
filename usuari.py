import hashlib
import getpass

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

class UsuariRegistrat(Usuari):
    """
    Classe que representa un usuari registrat de la biblioteca, heretant de Usuari.
    
    Afegeix dos camps nous:
        _contrasenya (str): Atribut protegit per la contrasenya encriptada.
        tipus_usuari (str): Tipus d'usuari, només pot ser 'lector' o 'admin'.

    Mètodes:
        __init__(nom, cognoms, dni, tipus_usuari='lector'):
            Inicialitza un usuari registrat, validant el tipus d'usuari.
        set_contrasenya():
            Demana la contrasenya oculta, l'encripta i la guarda.
        verificar_contrasenya(password) -> bool:
            Comprova si la contrasenya donada coincideix amb la guardada.
        encriptar_contrasenya(password) -> str:
            Encripta una contrasenya amb SHA-256 i retorna el hash hexadecimal.
        introduir_dades():
            Demana dades bàsics i la contrasenya (utilitza getpass).
    """

    def __init__(self, nom: str = "None", cognoms: str = "None", dni: str = "None", tipus_usuari: str = "lector"):
        super().__init__(nom, cognoms, dni)
        if tipus_usuari.lower() in ["lector", "admin"]:
            self.tipus_usuari = tipus_usuari.lower()
        else:
            self.tipus_usuari = "lector"
        self._contrasenya = None

    def encriptar_contrasenya(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def set_contrasenya(self):
        password = getpass.getpass("Introdueix la contrasenya: ")
        password_confirm = getpass.getpass("Confirma la contrasenya: ")
        if password == password_confirm:
            self._contrasenya = self.encriptar_contrasenya(password)
            print("Contrasenya guardada correctament.")
        else:
            print("Les contrasenyes no coincideixen. Torna-ho a intentar.")
            self.set_contrasenya()  # Demanar de nou

    def verificar_contrasenya(self, password: str) -> bool:
        if self._contrasenya is None:
            return False
        return self.encriptar_contrasenya(password) == self._contrasenya

    def introduir_dades(self):
        super().introduir_dades()
        tipus = input("Introdueix el tipus d'usuari (lector/admin): ").lower()
        if tipus in ["lector", "admin"]:
            self.tipus_usuari = tipus
        else:
            self.tipus_usuari = "lector"
        self.set_contrasenya()
