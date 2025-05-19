# README.md

## 📚 Projecte: Biblioteca

Aquest projecte en Python gestiona una biblioteca amb usuaris i llibres. Permet afegir, eliminar, llistar llibres i usuaris, així com gestionar préstecs de llibres per un màxim d’un mes i fins a 3 llibres per usuari.

---

### 🔧 Estructura del projecte

```
m0487_ra56_CognomAlumne/
├── biblioteca.py        # Classe principal amb la gestió de la base de dades
├── llibre.py            # Classe Llibre
├── usuari.py            # Classe Usuari
├── menu.py              # Menú de la biblioteca
├── bbdd.sqlite3         # Base de dades SQLite
├── test_biblioteca.py   # Tests unitaris (pendents d’implementar)
└── README.md            # Aquest fitxer
```

---

### 🧪 Requisits

- Python 3.x
- Mòduls: `sqlite3`, `datetime`, `re`

---

### 🚀 Com executar

1. Clona el repositori:
```bash
git clone https://github.com/usuari/m0487_ra56_CognomAlumne.git
cd m0487_ra56_CognomAlumne
```

2. Executa el programa:
```bash
python menu.py
```

---

### ✔️ Funcionalitats

- Afegir / eliminar / llistar usuaris
- Afegir / eliminar / llistar llibres
- Prestar llibres (fins a 3 per usuari i màxim 30 dies)
- Tornar llibres i veure quants dies han estat en préstec
- Validació de DNI (format espanyol)

---

### 🔍 Millores futures

- Validacions més estrictes de dades
- Tests unitaris amb unittest
- Control d’errors més complet
- Interfície gràfica (opcional)

---

### 👨‍🏫 Autor
*Dídac Garcia Molina*

Repositori GitHub: [enllaç al repo]

Afegit com a col·laborador: `frossell@xtec.cat`
