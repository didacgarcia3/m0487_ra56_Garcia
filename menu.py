from biblioteca import Biblioteca
from usuari_registrat import UsuariRegistrat  

def mostrar_menu_admin():
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

def mostrar_menu_lector():
    print("\n--- Menú Lector ---")
    print("1. Llistar llibres")
    print("2. Prestar llibre")
    print("3. Tornar llibre")
    print("0. Sortir")

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

# Programa principal
if __name__ == "__main__":
    biblio = Biblioteca()
    usuari = None

    while not usuari:
        usuari = login(biblio)

    while True:
        if usuari.tipus_usuari == "admin":
            mostrar_menu_admin()
            opcio = input("Selecciona una opció: ")
            if opcio == "1":
                nou = UsuariRegistrat()
                nou.introduir_dades()
                nou.set_contrasenya()
                if biblio.afegir_usuari(nou):
                    print("Usuari afegit.")
            elif opcio == "2":
                from llibre import Llibre
                titol = input("Títol: ")
                autor = input("Autor: ")
                llibre = Llibre(titol, autor)
                print(biblio.afegir_llibre(llibre))
            elif opcio == "3":
                biblio.imprimir_usuaris()
            elif opcio == "4":
                print(biblio.imprimir_llibres())
            elif opcio == "5":
                titol = input("Títol del llibre: ")
                dni = input("DNI del lector: ")
                print(biblio.prestar_llibre(titol, dni))
            elif opcio == "6":
                titol = input("Títol del llibre: ")
                print(biblio.tornar_llibre(titol))
            elif opcio == "7":
                dni = input("DNI de l’usuari a eliminar: ")
                print(biblio.eliminar_usuari(dni))
            elif opcio == "8":
                titol = input("Títol del llibre a eliminar: ")
                print(biblio.eliminar_llibre(titol))
            elif opcio == "9":
                dni = input("DNI de l’usuari: ")
                nom = input("Nou nom: ")
                cognoms = input("Nous cognoms: ")
                print(biblio.actualitzar_usuari(dni, nom, cognoms))
            elif opcio == "10":
                titol = input("Títol actual del llibre: ")
                nou_titol = input("Nou títol: ")
                nou_autor = input("Nou autor: ")
                print(biblio.actualitzar_llibre(titol, nou_titol, nou_autor))
            elif opcio == "0":
                print("Sortint... Adéu!")
                break
            else:
                print("Opció no vàlida.")
        
        elif usuari.tipus_usuari == "lector":
            mostrar_menu_lector()
            opcio = input("Selecciona una opció: ")
            if opcio == "1":
                print(biblio.imprimir_llibres())
            elif opcio == "2":
                titol = input("Títol del llibre: ")
                print(biblio.prestar_llibre(titol, usuari.dni))
            elif opcio == "3":
                titol = input("Títol del llibre: ")
                print(biblio.tornar_llibre(titol))
            elif opcio == "0":
                print("Sortint... Adéu!")
                break
            else:
                print("Opció no vàlida.")
