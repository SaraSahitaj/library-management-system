# Library Management System - Starter (Django)

This is the first part of the internship project built with **Python + Django** and prepared for **Visual Studio Code**.

## Included
- Register / Login / Logout
- Profile page
- User dashboard
- Book CRUD (add, edit, delete, list)
- Django admin panel
- SQLite by default
- Optional MySQL configuration

## 1. Open in VS Code
Extract the project zip and open the project folder in VS Code.

## 2. Create virtual environment
```bash
python -m venv venv
```

### Windows
```bash
venv\Scripts\activate
```

### Mac / Linux
```bash
source venv/bin/activate
```

## 3. Install packages
```bash
pip install -r requirements.txt
```

## 4. Copy environment file
Create a file named `.env` in the project root and copy the content from `.env.example`.

## 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 6. Create admin user
```bash
python manage.py createsuperuser
```

## 7. Start server
```bash
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

---

## MySQL setup (optional)
If you want to use MySQL instead of SQLite:

1. Create a MySQL database, for example: `library_management_db`
2. In `.env`, change:
```env
USE_MYSQL=True
MYSQL_DB=library_management_db
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```
3. Run migrations again:
```bash
python manage.py migrate
```

---

## Main pages
- `/` -> home
- `/accounts/register/` -> register
- `/accounts/login/` -> login
- `/dashboard/` -> dashboard
- `/books/` -> book list
- `/admin/` -> Django admin

The AI part can be added later as a separate app.
