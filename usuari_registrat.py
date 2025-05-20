import hashlib
import getpass

class Usuari:
    def __init__(self, nom="None", cognoms="None", dni="None"):
        self.nom = nom
        self.cognoms = cognoms
        self.dni = dni

    def imprimir_dades(self):
        return f"Nom: {self.nom}, Cognoms: {self.cognoms}, DNI: {self.dni}"

    def introduir_dades(self):
        self.nom = input("Introdueix el nom: ")
        self.cognoms = input("Introdueix els cognoms: ")
        self.dni = input("Introdueix el DNI: ")

class UsuariRegistrat(Usuari):
    """
    Representa un usuari registrat a la biblioteca.

    Atributs:
        _contrasenya (str): Contrasenya encriptada (variable protegida).
        tipus_usuari (str): Tipus d'usuari ('lector' o 'admin').

    Mètodes:
        set_contrasenya(): Demana la contrasenya de forma oculta, l'encripta i la guarda.
        verificar_contrasenya(password): Retorna True si la contrasenya és correcta.
        encriptar_contrasenya(password): Retorna el hash SHA-256 de la contrasenya.
        introduir_dades(): Demana les dades bàsiques i el tipus d'usuari.
    """

    def __init__(self, tipus_usuari="lector", **kwargs):
        super().__init__(**kwargs)  # Reutilitza el constructor de la classe base
        if tipus_usuari.lower() in ("lector", "admin"):
            self.tipus_usuari = tipus_usuari.lower()
        else:
            self.tipus_usuari = "lector"
        self._contrasenya = None

    def encriptar_contrasenya(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def set_contrasenya(self):
        while True:
            contrasenya = getpass.getpass("Introdueix la contrasenya: ")
            confirmacio = getpass.getpass("Confirma la contrasenya: ")
            if contrasenya == confirmacio:
                self._contrasenya = self.encriptar_contrasenya(contrasenya)
                print("Contrasenya guardada correctament.")
                break
            else:
                print("Les contrasenyes no coincideixen. Torna-ho a intentar.")

    def get_contrasenya(self):
        return self._contrasenya

    def verificar_contrasenya(self, password):
        if self._contrasenya is None:
            return False
        return self.encriptar_contrasenya(password) == self._contrasenya

    def introduir_dades(self):
        super().introduir_dades()
        tipus = input("Introdueix el tipus d'usuari (lector/admin): ").lower()
        if tipus in ("lector", "admin"):
            self.tipus_usuari = tipus
        else:
            self.tipus_usuari = "lector"
        # Es recomana posar contrasenya després amb set_contrasenya()
