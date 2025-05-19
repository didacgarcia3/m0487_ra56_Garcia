# biblioteca.py
import sqlite3
from llibre import Llibre
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuaris (
                dni TEXT PRIMARY KEY,
                nom TEXT,
                cognoms TEXT
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

    def afegir_usuari(self, usuari: Usuari):
        if not re.match(r"^\d{8}[A-HJ-NP-TV-Z]$", usuari.dni):
            return "DNI no vàlid."
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO usuaris VALUES (?, ?, ?)", (usuari.dni, usuari.nom, usuari.cognoms))
        self.conn.commit()
        return "Usuari afegit."

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
        cursor.execute("SELECT * FROM usuaris")
        return cursor.fetchall()

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
