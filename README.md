# 🐾 Pet Rescue Web Application (Django)

A full-stack web application built using Django to manage pet rescue operations, user interactions, and adoption workflows. The system enables users to browse pets, manage accounts, and communicate through integrated features.

---

## 🚀 Features

* 🐶 Pet listing and management system
* 👤 User authentication (accounts module)
* 💬 Chat functionality between users
* 🛡️ Trusted user feature implementation
* 📂 Modular Django app structure
* 🗄️ SQLite database integration

---

## 🛠️ Tech Stack

* Backend: Django (Python)
* Database: SQLite3
* Frontend: HTML, CSS (Django templates)
* Other: Django ORM

---

## 📁 Project Structure

```
petrescue1/
│── petrescue/
│   ├── manage.py
│   ├── db.sqlite3
│   ├── accounts/
│   ├── chat/
│   ├── pets/
│   ├── static/
│   ├── templates/
│   ├── petrescue/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   ├── wsgi.py
│── README.md
```

---

## ⚙️ Installation & Setup

1. Clone the repository

```
git clone https://github.com/muppalla03/petrescue1.git
cd petrescue1
```

2. Create a virtual environment

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```
pip install -r petrescue/requirements.txt
```

4. Apply migrations

```
python petrescue/manage.py migrate
```

5. Run the development server

```
python petrescue/manage.py runserver
```

6. Open in browser

```
http://127.0.0.1:8000/
```

---

## 🎯 Future Improvements

* Deploy on cloud platforms (Render / AWS / Railway)
* Implement real-time chat using WebSockets
* Improve UI/UX design
* Add role-based access (admin, rescuer, adopter)

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

---

## 📧 Contact

GitHub: https://github.com/muppalla03

---

⭐ If you found this project useful, consider giving it a star!
