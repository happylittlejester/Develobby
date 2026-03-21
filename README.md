# 🎯 Develobby

> Platforma społecznościowa dla hobbystów zbudowana w Django — odkrywaj, zarządzaj i rozwijaj swoje pasje.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-green?logo=django&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-38.9%25-orange?logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-34.6%25-blue?logo=css3&logoColor=white)

---

## 📖 O projekcie

**Develobby** to webowa aplikacja dla hobbystów, która pozwala użytkownikom rejestrować się, zarządzać swoimi pasjami, przeglądać dostępne hobbies oraz korzystać z wbudowanego sklepu. Projekt oferuje system kont z możliwością rozszerzenia do planu premium oraz panel administracyjny Django.

---

## ✨ Funkcje

- 🔐 **Rejestracja i logowanie** — system kont użytkowników z autentykacją
- 👤 **Profil użytkownika** — personalizacja i zarządzanie kontem
- 🎨 **Panel hobby** — dodawanie i zarządzanie własnymi pasjami
- 📚 **Baza hobby** — przeglądanie dostępnych kategorii hobby
- 🛒 **Sklep** — zakup produktów związanych z pasjami
- ⭐ **Plan Premium (Upgrade)** — rozszerzone funkcje dla wymagających użytkowników
- ❓ **FAQ** — odpowiedzi na najczęstsze pytania
- 🛠️ **Panel administracyjny** — zarządzanie aplikacją przez admina

---

## 🖼️ Zrzuty ekranu

<!-- SCREENSHOT: Strona główna — hero section z opisem platformy i CTA -->
### Strona główna
![Strona główna](screenshots/home.png)

<!-- SCREENSHOT: Widok panelu hobby po zalogowaniu -->
### Panel hobby
![Panel hobby](screenshots/hobby_panel.png)

<!-- SCREENSHOT: Strona z listą dostępnych hobby -->
### Przeglądanie hobby
![Lista hobby](screenshots/hobbies.png)

<!-- SCREENSHOT: Strona upgrade — porównanie planów Free vs Premium -->
### Plany i upgrade
![Upgrade](screenshots/upgrade.png)

<!-- SCREENSHOT: Sklep z produktami -->
### Sklep
![Sklep](screenshots/store.png)

<!-- SCREENSHOT: Strona profilu użytkownika -->
### Profil użytkownika
![Profil](screenshots/profile.png)

---

## 🛠️ Technologie

| Warstwa | Technologia |
|---|---|
| Backend | Python 3, Django |
| Frontend | HTML5, CSS3 |
| Baza danych | SQLite (domyślna Django) |
| Panel admina | Django Admin |

---

## 🚀 Instalacja i uruchomienie

### Wymagania

- Python 3.8+
- pip

### Kroki

1. **Sklonuj repozytorium**
   ```bash
   git clone https://github.com/ww30361/Develobby.git
   cd Develobby
   ```

2. **Utwórz i aktywuj wirtualne środowisko** *(zalecane)*
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Zainstaluj zależności**
   ```bash
   pip install django
   ```

4. **Przejdź do katalogu projektu**
   ```bash
   cd myproject
   ```

5. **Wykonaj migracje bazy danych**
   ```bash
   python manage.py migrate
   ```

6. **Utwórz konto administratora** *(opcjonalnie)*
   ```bash
   python manage.py createsuperuser
   ```

7. **Uruchom serwer deweloperski**
   ```bash
   python manage.py runserver
   ```

---

## 🌐 Dostępne adresy URL

| Adres | Opis |
|---|---|
| `http://127.0.0.1:8000/` | Strona główna |
| `http://127.0.0.1:8000/register/` | Rejestracja |
| `http://127.0.0.1:8000/login/` | Logowanie |
| `http://127.0.0.1:8000/profile/` | Profil użytkownika |
| `http://127.0.0.1:8000/hobby_panel/` | Panel zarządzania hobby |
| `http://127.0.0.1:8000/hobbies/` | Przeglądanie hobby |
| `http://127.0.0.1:8000/store/` | Sklep |
| `http://127.0.0.1:8000/upgrade` | Plany premium |
| `http://127.0.0.1:8000/faq` | FAQ |
| `http://127.0.0.1:8000/admin/` | Panel administratora |

---

## 📁 Struktura projektu

```
Develobby/
├── myproject/
│   ├── myproject/          # Konfiguracja projektu Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── [aplikacje]/        # Aplikacje Django (hobby, store, users itp.)
│   ├── templates/          # Szablony HTML
│   ├── static/             # Pliki CSS, JS, grafiki
│   └── manage.py
├── .gitignore
└── README.md
```
