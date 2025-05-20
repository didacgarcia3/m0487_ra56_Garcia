Clar! Aquí tens el teu README actualitzat i ajustat amb totes les novetats, preparat per copiar i enganxar:

````markdown
# Biblioteca - Gestió de Llibres i Usuaris amb SQLite3

Aquest projecte implementa una biblioteca digital que permet gestionar llibres i usuaris fent servir una base de dades SQLite3.  
Permet afegir, eliminar i llistar llibres i usuaris, així com gestionar préstecs i tornades de llibres.

---

## Funcionalitats

### Gestió de llibres:
- Afegir, llistar, eliminar i actualitzar llibres.
- Assignar un llibre en préstec a un usuari.
- Tornar un llibre a la biblioteca.

### Gestió d'usuaris:
- Afegir, llistar, eliminar i actualitzar usuaris.

### Ús de base de dades SQLite3:
- Els llibres i usuaris es guarden a `biblioteca.db`.
- Les taules es creen automàticament si no existeixen.
- Es fan consultes SQL per gestionar la informació.

### Control d'errors:
- Validació de dades amb `try-except`.
- Control d'errors per a DNIs repetits.
- Evita introduir dades incorrectes o buides.

### Autenticació i permisos:
- Login amb DNI i contrasenya.
- Diferenciació d’usuaris amb permisos d’administrador i lector.
- Menús separats per tipus d’usuari (`MenuAdmin` i `MenuLector`) basats en herència.

---

## Instal·lació i ús

- Clona aquest repositori i obre'l amb Visual Studio Code o un editor similar.
- Executa el programa principal amb:  
  ```bash
  python menu.py
````

* Introdueix el DNI i contrasenya per accedir.
* Segueix les opcions del menú segons el tipus d’usuari (admin o lector).

---

## Base de dades SQLite3

El programa utilitza una base de dades anomenada `biblioteca.db` amb dues taules principals:

* **Taula usuaris**

| id | nom   | cognoms | dni       | contrasenya      | tipus\_usuari |
| -- | ----- | ------- | --------- | ---------------- | ------------- |
| 1  | Paco  | Ross    | 12345678A | \*\*\*\*\*\*\*\* | admin         |
| 2  | Maria | Tendas  | 87654321B | \*\*\*\*\*\*\*\* | lector        |

* **Taula llibres**

| id | titol | autor   | dni\_prestec |
| -- | ----- | ------- | ------------ |
| 1  | 1984  | Orwell  | 12345678A    |
| 2  | Dune  | Herbert | 0            |

Si `dni_prestec = "0"`, el llibre està disponible.
Si `dni_prestec` conté un DNI, el llibre està en préstec.

---

## Menú principal

En iniciar sessió, es mostra un menú segons el tipus d’usuari:

### Menú Administrador

1. Afegir usuari
2. Afegir llibre
3. Llistar usuaris
4. Llistar llibres
5. Prestar llibre
6. Tornar llibre
7. Eliminar usuari
8. Eliminar llibre
9. Actualitzar usuari
10. Actualitzar llibre
11. Sortir

### Menú Lector

1. Llistar llibres
2. Prestar llibre
3. Tornar llibre
4. Sortir

---

## Tecnologies utilitzades

* Python 3
* SQLite3
* Gestió d'errors amb `try-except`
* Unittest per proves automatitzades
* Programació orientada a objectes (herència en menús)

---

## Millores implementades i pendents

### Implementades:

* Login segur amb contrasenya.
* Menús diferenciats per permisos (admin/lector).
* Actualització de dades d’usuaris i llibres.
* Tests automatitzats amb unittest.

### Pendents:

* Validar format oficial del DNI.
* Controlar límits en préstecs (temps i quantitat).
* Afegir interfície gràfica amb Tkinter.
* Implementar API REST amb FastAPI.
* Exportar i importar dades a CSV o JSON.

---

## Com realitzar tests

Els tests es troben a la carpeta `tests/` i cobreixen funcionalitats claus.
Per executar-los, utilitza:

```bash
python -m unittest discover tests
```

---

## Crèdits

Creat per **Dídac Garcia Molina**, 2025.
[El Teu GitHub](https://github.com/didacgarcia3/m0487_ra56_Garcia.git)

