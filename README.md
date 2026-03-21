# 🎯 Develobby

> A social platform for hobbyists built with Django — discover, manage, and grow your passions.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-green?logo=django&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-38.9%25-orange?logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-34.6%25-blue?logo=css3&logoColor=white)

---

## 📖 About the Project
 
**Develobby** is a web application for hobbyists that allows users to register, manage their passions, browse available hobbies, and use the built-in store. The project features a user account system with the option to upgrade to a premium plan.

---

## ✨ Features
 
- 🔐 **Registration & Login** — user account system
- 👤 **User Profile** — account management
- 🎨 **Hobby Panel** — add and manage your own hobbies
- 📚 **Hobby Browser** — explore available hobby categories
- 🛒 **Store** — purchase products related to your passions (cooming soon)
- ⭐ **Premium Plan (Upgrade)** — extended features for power users (cooming soon)
- ❓ **FAQ** — answers to the most common questions
- 🛠️ **Admin Panel** — application management via Django Admin

---

## 🖼️ Screenshots

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

## 🛠️ Tech Stack
 
| Layer | Technology |
|---|---|
| Backend | Python 3, Django |
| Frontend | HTML5, CSS3 |
| Database | SQLite (Django default) |
| Admin Panel | Django Admin |

---

## 🚀 Installation & Setup
 
### Requirements
 
- Python 3.8+
- pip
 
### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ww30361/Develobby.git
   ```

2. **Create and activate a virtual environment****
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django requests pillow
   ```

4. **Navigate to the project directory**
   ```bash
   cd myproject
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

---

## 🌐 Available URLs
 
| URL | Description |
|---|---|
| `http://127.0.0.1:8000/` | Home page |
| `http://127.0.0.1:8000/register/` | Registration |
| `http://127.0.0.1:8000/login/` | Login |
| `http://127.0.0.1:8000/profile/` | User profile |
| `http://127.0.0.1:8000/hobby_panel/` | Hobby management panel |
| `http://127.0.0.1:8000/hobbies/` | Browse hobbies |
| `http://127.0.0.1:8000/store/` | Store |
| `http://127.0.0.1:8000/upgrade` | Premium plans |
| `http://127.0.0.1:8000/faq` | FAQ |

---

## 📁 Project Structure

```
Develobby/
├── myproject/
│   ├── myapp               # Django applications (hobby, store, users itp.)
│       ├── static
│           ├── css         # css files
│           └── img         # images
│       ├── templates
│           └── myapp       # html files
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── models.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
│   ├── myproject/          # konfiguracja projektu Django
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
│   └── manage.py
├── .gitignore
└── README.md

```
