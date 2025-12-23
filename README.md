# Task Management REST API 🚀

A backend **REST API** built using **FastAPI** for managing **users, projects, and tasks**.  
The application implements **JWT authentication**, **PostgreSQL persistence**, and follows a **clean modular architecture**.  
It is deployed on **Render** and provides interactive API documentation via **Swagger UI**.

---

## 🌐 Live Demo

**Base URL:**  
https://task-project-management-rest-api.onrender.com

**Swagger UI (API Docs):**  
https://task-project-management-rest-api.onrender.com/docs

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI  
- **Language:** Python 3.13  
- **Database:** PostgreSQL  
- **ORM:** SQLAlchemy  
- **Authentication:** JWT (OAuth2 Password Flow)  
- **Server:** Gunicorn  
- **Deployment:** Render  

---

## 📌 Features

- User Registration & Login
- JWT-based Authentication
- Project Management (Create, Read)
- Task Management (Create, Read, Assign to Project)
- Relationship Handling  
  - One User → Many Projects  
  - One Project → Many Tasks
- Automatic API Documentation (Swagger UI)

---

## 📂 Project Structure
app/
├── api/
│ ├── auth.py
│ ├── users.py
│ ├── projects.py
│ └── tasks.py
│
├── models/
│ ├── user.py
│ ├── project.py
│ └── task.py
│
├── schemas/
│ ├── user.py
│ ├── project.py
│ └── task.py
│
├── db/
│ ├── base.py
│ ├── session.py
│ └── init_db.py
│
├── core/
│ └── config.py
│
└── main.py

---

## 🔐 Authentication Flow

1. User registers via `/auth/register`
2. User logs in via `/auth/login`
3. API returns a **JWT access token**
4. Token must be passed in request headers for protected routes

**Header Format:**

---

## 📌 API Endpoints Overview

### 🔑 Auth
- `POST /auth/register` – Register a new user  
- `POST /auth/login` – Login and receive JWT token  

### 👤 Users
- `GET /users/me` – Get logged-in user details  

### 📁 Projects
- `POST /projects/` – Create a project  
- `GET /projects/` – Get all projects  

### ✅ Tasks
- `POST /tasks/` – Create a task  
- `GET /tasks/` – Get all tasks  

---

## 🧪 Example Request

### Create Project

**POST** `/projects/`

```json
{
  "name": "Task Manager",
  "description": "Backend API Project"
}
🗄️ Database

PostgreSQL hosted on Render.

Tables

users

projects

tasks

Relationships

One User → Many Projects

One Project → Many Tasks
⚙️ Environment Variables

Create a .env file and configure the following:

DATABASE_URL=postgresql://<username>:<password>@<host>/<db_name>
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

🚀 Run Locally
git clone https://github.com/aadiiiitii001/Task-Project-Management-REST-API.git
cd Task-Project-Management-REST-API

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload

📖 API Documentation

Once the server is running, access Swagger UI at:

http://127.0.0.1:8000/docs

