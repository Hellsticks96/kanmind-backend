# 🗂️ Kanban Backend

This is the backend for a **Kanban task management system**, built using Django and Django REST Framework. It provides a RESTful API for managing boards, columns, and tasks.

---

## 🚀 Features

- ✅ CRUD operations for Boards, Columns, and Tasks
- ✅ Token-based Authentication
- ✅ DRF (Django REST Framework) for API development
- ✅ Admin interface for data management

---

## 🛠️ Tech Stack

- **Python 3**
- **Django**
- **Django REST Framework**
- **SQLite3** (default DB for development)

---

## 📦 Installation

> Clone the repository and set up the virtual environment:

```bash
git clone https://github.com/yourusername/kanban-backend.git
cd kanban-backend
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## ⚙️ Running the Project

```bash
python manage.py migrate
python manage.py runserver
```

By default, the server will run at: `http://127.0.0.1:8000/`

---

## 🧪 API Overview

Here's a brief look at the available endpoints (check `tasks/urls.py` for more details):

| Endpoint               | Method | Description                |
|------------------------|--------|----------------------------|
| `/api/tasks/`          | GET/POST | List or create tasks     |
| `/api/tasks/<id>/`     | GET/PUT/DELETE | Task detail view   |
| `/api/boards/`         | GET/POST | List or create boards    |
| `/api/columns/`        | GET/POST | List or create columns   |
| `/api/token/`          | POST   | Obtain JWT tokens         |
| `/api/token/refresh/`  | POST   | Refresh JWT token         |

---

## 🔐 Authentication

Uses **JWT Authentication**. To authenticate:

1. Obtain a token:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/token/ -d "username=youruser&password=yourpass"
   ```

2. Use the token in headers:
   ```
   Authorization: Bearer <your_token>
   ```

---

## 🛡️ Admin Access

To access Django Admin:
```bash
python manage.py createsuperuser
```
Then log in at `http://127.0.0.1:8000/admin/`

---

## 📁 Project Structure

```
kanban-backend/
├── kanban_project/
│   ├── settings.py
│   ├── urls.py
├── tasks/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
├── db.sqlite3
├── manage.py
```

---

## 🧾 License

This project is licensed under the MIT License.
