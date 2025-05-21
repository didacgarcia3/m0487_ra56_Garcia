# biblioteca.py
import sqlite3
from llibre import Llibre
from usuari_registrat import UsuariRegistrat
from usuari import Usuari
from datetime import datetime
import re
import hashlib

class Biblioteca:
    def __init__(self):
        self.conn = sqlite3.connect("bbdd.sqlite3")
        self.crear_taules()
        self.crear_admin_per_defecte()

    def crear_taules(self):
        cursor = self.conn.cursor()
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

    def crear_admin_per_defecte(self):
        cursor = self.conn.cursor()
        dni_admin = "00000000A"
        cursor.execute("SELECT * FROM usuaris WHERE dni = ?", (dni_admin,))
        if cursor.fetchone() is None:
            # Hashejar contrasenya per seguretat
            contrasenya = self.hashear_contrasenya("admin123")
            cursor.execute('''
                INSERT INTO usuaris (dni, nom, cognoms, tipus_usuari, contrasenya)
                VALUES (?, ?, ?, ?, ?)
            ''', (dni_admin, "Admin", "Default", "admin", contrasenya))
            self.conn.commit()

    def hashear_contrasenya(self, contrasenya):
        return hashlib.sha256(contrasenya.encode("utf-8")).hexdigest()

    def verificar_contrasenya(self, contrasenya_guardada, contrasenya_introduida):
        return contrasenya_guardada == self.hashear_contrasenya(contrasenya_introduida)

    def afegir_usuari(self, usuari: Usuari) -> bool:
        if not isinstance(usuari, UsuariRegistrat):
            print("Error: només es poden afegir usuaris registrats.")
            return False

        if usuari.tipus_usuari not in ["lector", "admin"]:
            print("Error: tipus_usuari ha de ser 'lector' o 'admin'.")
            return False

        if not re.match(r"^\d{8}[A-HJ-NP-TV-Z]$", usuari.dni):
            print("Error: DNI no vàlid.")
            return False

        if usuari.get_contrasenya() is None:
            print("Error: contrasenya no definida.")
            return False

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuaris WHERE dni = ?", (usuari.dni,))
        if cursor.fetchone() is not None:
            print("Error: l'usuari ja existeix.")
            return False

        # ❗️No volver a encriptar la contrasenya
        contrasenya_xifrada = usuari.get_contrasenya()

        cursor.execute('''
            INSERT INTO usuaris (dni, nom, cognoms, tipus_usuari, contrasenya)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuari.dni, usuari.nom, usuari.cognoms, usuari.tipus_usuari, contrasenya_xifrada))

        self.conn.commit()
        return True

        

    def canviar_contrasenya(self, dni, contrasenya_nova):
        cursor = self.conn.cursor()
        contrasenya_xifrada = self.hashear_contrasenya(contrasenya_nova)
        cursor.execute("UPDATE usuaris SET contrasenya = ? WHERE dni = ?", (contrasenya_xifrada, dni))
        self.conn.commit()
        return "Contrasenya actualitzada correctament."

    def afegir_llibre(self, llibre: Llibre) -> str:
        cursor = self.conn.cursor()
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
            estat = "Disponible" if not dni_prestec else f"Prestat a {dni_prestec}"
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
        cursor.execute("SELECT COUNT(*) FROM llibres WHERE dni_prestec = ?", (dni,))
        if cursor.fetchone()[0] >= 3:
            return "L’usuari ja té 3 llibres en préstec."

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
