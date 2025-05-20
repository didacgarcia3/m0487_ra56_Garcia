# menu.py
from biblioteca import Biblioteca
from usuari_registrat import UsuariRegistrat

class MenuBase:
    def __init__(self, biblioteca: Biblioteca, usuari: UsuariRegistrat):
        self.biblioteca = biblioteca
        self.usuari = usuari
    
    def mostrar_menu(self):
        raise NotImplementedError("Aquest mètode ha de ser sobreescrit.")
    
    def executar_opcio(self, opcio):
        raise NotImplementedError("Aquest mètode ha de ser sobreescrit.")

    def run(self):
        while True:
            self.mostrar_menu()
            opcio = input("Selecciona una opció: ")
            if opcio == "0":
                print("Sortint... Adéu!")
                break
            self.executar_opcio(opcio)


class MenuAdmin(MenuBase):
    def mostrar_menu(self):
        print("\n--- Menú Administrador ---")
        print("1. Afegir usuari")
        print("2. Afegir llibre")
        print("3. Llistar usuaris")
        print("4. Llistar llibres")
        print("5. Prestar llibre")
        print("6. Tornar llibre")
        print("7. Eliminar usuari")
        print("8. Eliminar llibre")
        print("9. Actualitzar usuari")
        print("10. Actualitzar llibre")
        print("0. Sortir")

    def executar_opcio(self, opcio):
        if opcio == "1":
            nou = UsuariRegistrat()
            nou.introduir_dades()
            nou.set_contrasenya()
            if self.biblioteca.afegir_usuari(nou):
                print("Usuari afegit.")
        elif opcio == "2":
            from llibre import Llibre
            titol = input("Títol: ")
            autor = input("Autor: ")
            llibre = Llibre(titol, autor)
            print(self.biblioteca.afegir_llibre(llibre))
        elif opcio == "3":
            self.biblioteca.imprimir_usuaris()
        elif opcio == "4":
            print(self.biblioteca.imprimir_llibres())
        elif opcio == "5":
            titol = input("Títol del llibre: ")
            dni = input("DNI del lector: ")
            print(self.biblioteca.prestar_llibre(titol, dni))
        elif opcio == "6":
            titol = input("Títol del llibre: ")
            print(self.biblioteca.tornar_llibre(titol))
        elif opcio == "7":
            dni = input("DNI de l’usuari a eliminar: ")
            print(self.biblioteca.eliminar_usuari(dni))
        elif opcio == "8":
            titol = input("Títol del llibre a eliminar: ")
            print(self.biblioteca.eliminar_llibre(titol))
        elif opcio == "9":
            dni = input("DNI de l’usuari: ")
            nom = input("Nou nom: ")
            cognoms = input("Nous cognoms: ")
            print(self.biblioteca.actualitzar_usuari(dni, nom, cognoms))
        elif opcio == "10":
            titol = input("Títol actual del llibre: ")
            nou_titol = input("Nou títol: ")
            nou_autor = input("Nou autor: ")
            print(self.biblioteca.actualitzar_llibre(titol, nou_titol, nou_autor))
        else:
            print("Opció no vàlida.")


class MenuLector(MenuBase):
    def mostrar_menu(self):
        print("\n--- Menú Lector ---")
        print("1. Llistar llibres")
        print("2. Prestar llibre")
        print("3. Tornar llibre")
        print("0. Sortir")

    def executar_opcio(self, opcio):
        if opcio == "1":
            print(self.biblioteca.imprimir_llibres())
        elif opcio == "2":
            titol = input("Títol del llibre: ")
            print(self.biblioteca.prestar_llibre(titol, self.usuari.dni))
        elif opcio == "3":
            titol = input("Títol del llibre: ")
            print(self.biblioteca.tornar_llibre(titol))
        else:
            print("Opció no vàlida.")


def login(biblio: Biblioteca):
    print("== LOGIN ==")
    dni = input("DNI: ")
    contrasenya = input("Contrasenya: ")

    cursor = biblio.conn.cursor()
    cursor.execute("SELECT nom, cognoms, contrasenya, tipus_usuari FROM usuaris WHERE dni = ?", (dni,))
    resultat = cursor.fetchone()

    if resultat:
        nom, cognoms, contrasenya_guardada, tipus = resultat
        usuari = UsuariRegistrat(nom=nom, cognoms=cognoms, dni=dni, tipus_usuari=tipus)
        usuari._contrasenya = contrasenya_guardada  # simulant accés protegit
        if usuari.verificar_contrasenya(contrasenya):
            print(f"\nBenvingut/da, {nom} ({tipus})!")
            return usuari
        else:
            print("Contrasenya incorrecta.")
    else:
        print("Usuari no trobat.")
    return None


if __name__ == "__main__":
    biblio = Biblioteca()
    usuari = None

    while not usuari:
        usuari = login(biblio)

    if usuari.tipus_usuari == "admin":
        menu = MenuAdmin(biblio, usuari)
    else:
        menu = MenuLector(biblio, usuari)
    menu.run()
