# biblioteca.py
import sqlite3
from llibre import Llibre
from usuari_registrat import UsuariRegistrat
from usuari import Usuari
from datetime import datetime, timedelta
import re

class Biblioteca:
    """
    Classe que gestiona la biblioteca, incloent usuaris, llibres i la base de dades.

    Atributs:
        conn (sqlite3.Connection): Connexió a la base de dades SQLite.

    Mètodes:
        __init__():
            Inicialitza la connexió a la base de dades i crea les taules si no existeixen.
        crear_taules():
            Crea les taules per usuaris i llibres a la base de dades.
        afegir_usuari(usuari: Usuari) -> str:
            Afegeix un usuari a la base de dades després de validar el DNI.
        afegir_llibre(llibre: Llibre) -> str:
            Afegeix un llibre a la base de dades.
        imprimir_usuaris() -> str:
            Retorna una cadena amb la llista d'usuaris.
        imprimir_llibres(filtre: str = "tots") -> str:
            Retorna una cadena amb la llista de llibres, segons el filtre.
        eliminar_usuari(dni: str) -> str:
            Elimina un usuari pel DNI.
        eliminar_llibre(titol: str) -> str:
            Elimina un llibre pel títol.
        prestar_llibre(titol: str, dni: str) -> str:
            Assigna un llibre a un usuari si compleix les condicions.
        tornar_llibre(titol: str) -> str:
            Marca un llibre com retornat.
    """
    
    def __init__(self):
        self.conn = sqlite3.connect("bbdd.sqlite3")
        self.crear_taules()

    def crear_taules(self):
        cursor = self.conn.cursor()
        # Comprovar si cal afegir columnes noves
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuaris (
                dni TEXT PRIMARY KEY,
                nom TEXT,
                cognoms TEXT,
                contrasenya TEXT,
                tipus_usuari TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS llibres (
                titol TEXT PRIMARY KEY,
                autor TEXT,
                dni_prestec TEXT,
                data_prestec TEXT
            )
        ''')
        self.conn.commit()


    def afegir_usuari(self, usuari: Usuari) -> bool:
        """
        Afegeix un usuari a la base de dades després de validar el DNI i el tipus d'usuari.
        Només accepta instàncies de UsuariRegistrat.
        
        Args:
            usuari (Usuari): Objecte Usuari o UsuariRegistrat a afegir.

        Retorna:
            bool: True si l'usuari s'ha afegit correctament, False en cas contrari.
        """
        # Validació instància
        if not isinstance(usuari, UsuariRegistrat):
            print("Error: només es poden afegir usuaris registrats.")
            return False
        
        # Validar tipus_usuari
        if usuari.tipus_usuari not in ["lector", "admin"]:
            print("Error: tipus_usuari ha de ser 'lector' o 'admin'.")
            return False
        
        # Validar DNI amb regex
        if not re.match(r"^\d{8}[A-HJ-NP-TV-Z]$", usuari.dni):
            print("Error: DNI no vàlid.")
            return False
        
        # Aquí podríem afegir més validacions, com verificar que la contrasenya està definida
        if usuari.get_contrasenya() is None:
            print("Error: contrasenya no definida.")
            return False
        
        cursor = self.conn.cursor()
        
        # Comprovar que no existeix un usuari amb el mateix DNI
        cursor.execute("SELECT * FROM usuaris WHERE dni = ?", (usuari.dni,))
        if cursor.fetchone() is not None:
            print("Error: l'usuari ja existeix.")
            return False
        
        # Afegim l'usuari a la taula usuaris, ara incloent tipus_usuari i contrasenya (xifrada)
        cursor.execute('''
            INSERT INTO usuaris (dni, nom, cognoms, tipus_usuari, contrasenya)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuari.dni, usuari.nom, usuari.cognoms, usuari.tipus_usuari, usuari.get_contrasenya()))
        
        self.conn.commit()
        return True


    def afegir_llibre(self, llibre: Llibre) -> str:
        cursor = self.conn.cursor()
        # Guardem NULL real, no la cadena "None"
        cursor.execute(
            "INSERT INTO llibres (titol, autor, dni_prestec, data_prestec) VALUES (?, ?, NULL, NULL)",
            (llibre.titol, llibre.autor)
        )
        self.conn.commit()
        return "Llibre afegit."


    def imprimir_usuaris(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT dni, nom, cognoms, tipus_usuari FROM usuaris")
        usuaris = cursor.fetchall()
    
        if not usuaris:
            print("No hi ha usuaris registrats.")
            return
    
        print(f"{'DNI':<12} {'Nom':<15} {'Cognoms':<20} {'Tipus Usuari':<10}")
        print("-" * 60)
        for dni, nom, cognoms, tipus in usuaris:
            print(f"{dni:<12} {nom:<15} {cognoms:<20} {tipus:<10}")

    def imprimir_llibres(self) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT titol, autor, dni_prestec FROM llibres")
        llibres = cursor.fetchall()
        resultat = ""
        for titol, autor, dni_prestec in llibres:
            if not dni_prestec or dni_prestec == "None":
                estat = "Disponible"
            else:
                estat = f"Prestat a {dni_prestec}"
            resultat += f"{titol} - {autor} - {estat}\n"
        return resultat

    def eliminar_usuari(self, dni):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM usuaris WHERE dni = ?", (dni,))
        self.conn.commit()
        return "Usuari eliminat."

    def eliminar_llibre(self, titol):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM llibres WHERE titol = ?", (titol,))
        self.conn.commit()
        return "Llibre eliminat."

    def prestar_llibre(self, titol, dni):
        cursor = self.conn.cursor()
    
        # Comprovar si l'usuari ja té 3 llibres
        cursor.execute("SELECT COUNT(*) FROM llibres WHERE dni_prestec = ?", (dni,))
        if cursor.fetchone()[0] >= 3:
            return "L’usuari ja té 3 llibres en préstec."
    
        # Assignar el préstec si el llibre està disponible
        data_prestec = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            UPDATE llibres
            SET dni_prestec = ?, data_prestec = ?
            WHERE titol = ? AND dni_prestec IS NULL
        """, (dni, data_prestec, titol))
    
        if cursor.rowcount == 0:
            return "El llibre ja està en préstec o no existeix."
    
        self.conn.commit()
        return "Llibre prestat correctament."


    def tornar_llibre(self, titol):
        cursor = self.conn.cursor()
        cursor.execute("SELECT data_prestec FROM llibres WHERE titol = ?", (titol,))
        data = cursor.fetchone()
        if data:
            data_prestec = datetime.strptime(data[0], "%Y-%m-%d")
            dies = (datetime.now() - data_prestec).days
            cursor.execute("UPDATE llibres SET dni_prestec = NULL, data_prestec = NULL WHERE titol = ?", (titol,))
            self.conn.commit()
            return f"Llibre tornat. Dies en préstec: {dies}"
        return "El llibre no està en préstec."

    def actualitzar_usuari(self, dni: str, nou_nom: str, nous_cognoms: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuaris WHERE dni = ?", (dni,))
        if cursor.fetchone() is None:
            return "Usuari no trobat."
        cursor.execute(
            "UPDATE usuaris SET nom = ?, cognoms = ? WHERE dni = ?",
            (nou_nom, nous_cognoms, dni)
        )
        self.conn.commit()
        return "Usuari actualitzat."


    def actualitzar_llibre(self, titol_actual: str, nou_titol: str, nou_autor: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM llibres WHERE titol = ?", (titol_actual,))
        if cursor.fetchone() is None:
            return "Llibre no trobat."
    
        # Si el nou títol és diferent, s’ha d’eliminar i tornar a inserir
        if titol_actual != nou_titol:
            cursor.execute("DELETE FROM llibres WHERE titol = ?", (titol_actual,))
            cursor.execute(
                "INSERT INTO llibres (titol, autor, dni_prestec, data_prestec) VALUES (?, ?, NULL, NULL)",
                (nou_titol, nou_autor)
            )
        else:
            cursor.execute("UPDATE llibres SET autor = ? WHERE titol = ?", (nou_autor, titol_actual))
    
        self.conn.commit()
        return "Llibre actualitzat."

