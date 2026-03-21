# 🎯 Develobby

> A social platform for hobbyists built with Django — discover, manage, and grow your passions.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-green?logo=django&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-38.9%25-orange?logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-34.6%25-blue?logo=css3&logoColor=white)

---

## 📖 About the Project
 
**Develobby** is a web application for hobbyists that combines passion management with gamification mechanics. Users register, choose their hobbies, complete challenges, and earn experience points (XP) that translate into levels and unique unlockable titles. The app integrates with the National Bank of Poland API, offers a shop with hobby-related products..

---

## ✨ Features
 
### 👤 User Profile
 
The profile is the center of each user's progress. It displays:
 
- **Level & Title** — as users earn XP, they level up and unlock unique titles. The title is prominently shown on the profile as a mark of achievement.
- **XP Progress Bar** — a visual indicator showing how many points separate the user from the next level.
- **Hobby Progress** — each added hobby displays its individual progress as a percentage, reflecting the user's engagement and completed challenges.
 
---
 
### 🎨 Hobbies Panel
 
The main hub for managing passions. From this panel, users can:
 
- **Add new hobbies** — assigning hobby to a profile
- **Remove hobbies** — drop passions they're no longer interested in
 
---
 
### 🏆 My Hobbies — Challenges & XP
 
Every hobby has a set of **challenges** — specific tasks to complete within that passion. The system works as follows:
 
- The user browses available challenges for their hobbies
- After completing a challenge and marking it as done, they receive a **reward in the form of XP points**
- Earned XP updates the hobby's progress (shown as a percentage) as well as the overall account level
- Regularly completing challenges leads to levelling up and unlocking new titles
 
---
 
### 🛒 Store
 
A built-in shop with tools and accessories related to hobbies. Key features:
 
- **Browse by category** — products organized thematically, making it easy to find accessories suited to a specific passion
- **Product cards** — each product presented with a description and price
- **NBP API integration** — prices can be displayed and converted using live exchange rates fetched from the **National Bank of Poland API**, always providing up-to-date currency conversion (PLN ↔ EUR, USD, and more)
 
---
 
### ⭐ Upgrade
 
Users can upgrade their account to a premium plan, unlocking additional platform features. Key features:

- **Premium Plan** — the upgrade page offers **3 plans at different price points**. Prices are displayed in your preferred currency and can be adjusted based on current exchange rates thanks to live exchange rates fetched from the **NBP API**.
 
---

### 💱 NBP API Integration
 
The application connects to the public **National Bank of Poland API** (`api.nbp.pl`), fetching live exchange rates in real time. This means:
 
- Product prices in the store can be automatically converted to the user's preferred currency
- Rates are always current — pulled directly from the official NBP source
- Users see values in the currency they care about, without manual conversion
 
---

## 🖼️ Screenshots

<!-- SCREENSHOT: homepage-->
### Homepage 
<img width="1848" height="923" alt="homepage" src="https://github.com/user-attachments/assets/116982fc-24c7-45f8-b297-bbc894f7189c" />

<!-- SCREENSHOT: upgrade-->
### Plan selection
<img width="1851" height="945" alt="plan" src="https://github.com/user-attachments/assets/7b991fa1-6fa1-4fa8-8fcf-924837141c02" />

<!-- SCREENSHOT: registration-->
### Registration
<img width="1855" height="944" alt="registration" src="https://github.com/user-attachments/assets/e8eaa6d1-fa4a-4cde-9e5f-1fd8a5411b95" />

<!-- SCREENSHOT: profile_1, profile_2-->
### Profile
<img width="1842" height="929" alt="profile_1" src="https://github.com/user-attachments/assets/6ccc72f3-80d6-421c-b13e-b1efc942bc8b" />
<img width="1857" height="843" alt="profile_2" src="https://github.com/user-attachments/assets/54bef94f-8fab-44a4-b256-62e1eb90d2ac" />

<!-- SCREENSHOT: my_hobbies -->
### My hobbies
<img width="1842" height="939" alt="my_hobbies" src="https://github.com/user-attachments/assets/77320d61-449b-4882-b25c-7df04b13985b" />
<img width="1845" height="941" alt="my_hobbies_2" src="https://github.com/user-attachments/assets/569b11d5-8841-4ce8-8a84-7cfe57289568" />

<!-- SCREENSHOT: hobbies_panel -->
### Hobbies panel
<img width="1840" height="946" alt="hobbies_panel" src="https://github.com/user-attachments/assets/424aa8be-4c13-48ef-b58b-44ae58990959" />

<!-- SCREENSHOT: store -->
### Store
<img width="1834" height="942" alt="store" src="https://github.com/user-attachments/assets/fced57a6-cc9c-4477-b146-f00371b39a71" />

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

2. **Create and activate a virtual environment**
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
│   ├── myapp               # Django applications (hobby, store, users etc.)
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
│   ├── myproject/          # Django project configuration
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
│   └── manage.py
├── .gitignore
└── README.md

```
