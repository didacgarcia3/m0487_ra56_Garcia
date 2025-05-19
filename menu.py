# menu.py
from biblioteca import Biblioteca
from llibre import Llibre
from usuari import Usuari

def mostrar_menu():
    print("""
    --- Menú Biblioteca ---
    1. Afegir usuari
    2. Afegir llibre
    3. Llistar usuaris
    4. Llistar llibres
    5. Eliminar usuari
    6. Eliminar llibre
    7. Prestar llibre
    8. Tornar llibre
    9. Actualitzar usuari
    10. Actualitzar llibre
    0. Sortir
    """)

biblioteca = Biblioteca()

while True:
    mostrar_menu()
    opcio = input("Selecciona una opció: ")

    if opcio == "1":
        usuari = Usuari()
        usuari.introduir_dades()
        print(biblioteca.afegir_usuari(usuari))

    elif opcio == "2":
        llibre = Llibre()
        llibre.introduir_dades()
        print(biblioteca.afegir_llibre(llibre))

    elif opcio == "3":
        usuaris = biblioteca.imprimir_usuaris()
        for u in usuaris:
            print(f"{u[0]} - {u[1]} {u[2]}")

    elif opcio == "4":
        print(biblioteca.imprimir_llibres())

    elif opcio == "5":
        dni = input("Introdueix el DNI de l’usuari a eliminar: ")
        print(biblioteca.eliminar_usuari(dni))

    elif opcio == "6":
        titol = input("Introdueix el títol del llibre a eliminar: ")
        print(biblioteca.eliminar_llibre(titol))

    elif opcio == "7":
        titol = input("Introdueix el títol del llibre: ")
        dni = input("Introdueix el DNI de l’usuari: ")
        print(biblioteca.prestar_llibre(titol, dni))

    elif opcio == "8":
        titol = input("Introdueix el títol del llibre a retornar: ")
        print(biblioteca.tornar_llibre(titol))

    elif opcio == "9":
        dni = input("Introdueix el DNI de l’usuari a actualitzar: ")
        nou_nom = input("Nou nom: ")
        nous_cognoms = input("Nous cognoms: ")
        print(biblioteca.actualitzar_usuari(dni, nou_nom, nous_cognoms))

    elif opcio == "10":
        titol = input("Introdueix el títol del llibre a actualitzar: ")
        nou_titol = input("Nou títol: ")
        nou_autor = input("Nou autor: ")
        print(biblioteca.actualitzar_llibre(titol, nou_titol, nou_autor))

    elif opcio == "0":
        print("Sortint...")
        break

    else:
        print("Opció no vàlida.")

   
    
