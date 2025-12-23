##Task Management REST API

A backend REST API built using FastAPI for managing users, projects, and tasks.
The application implements JWT authentication, PostgreSQL persistence, and follows a clean modular architecture.
The project is deployed on Render and exposes interactive API documentation using Swagger.

🌐 Live Demo

Base URL:
'''
https://task-project-management-rest-api.onrender.com
'''

Swagger UI (API Docs):

https://task-project-management-rest-api.onrender.com/docs

🛠️ Tech Stack

Backend Framework: FastAPI

Database: PostgreSQL

ORM: SQLAlchemy

Authentication: JWT (OAuth2 Password Flow)

Server: Gunicorn

Deployment: Render

Language: Python 3.13

📌 Features

User Registration & Login

JWT-based Authentication

Project Management (Create, Read)

Task Management (Create, Read, Assign to Project)

Relationship handling (User → Projects → Tasks)

Automatic API Documentation (Swagger)

📂 Project Structure
app/
├── api/
│   ├── auth.py
│   ├── users.py
│   ├── projects.py
│   └── tasks.py
│
├── models/
│   ├── user.py
│   ├── project.py
│   └── task.py
│
├── schemas/
│   ├── user.py
│   ├── project.py
│   └── task.py
│
├── db/
│   ├── base.py
│   ├── session.py
│   └── init_db.py
│
├── core/
│   └── config.py
│
└── main.py


🔐 Authentication Flow

User registers using /auth/register

User logs in using /auth/login

API returns JWT access token

Token is passed in request headers for protected routes

Authorization: Bearer <access_token>

📌 API Endpoints Overview
🔑 Auth

POST /auth/register – Register user

POST /auth/login – Login & get JWT token

👤 Users

GET /users/me – Get logged-in user details

📁 Projects

POST /projects/ – Create project

GET /projects/ – Get all projects

✅ Tasks

POST /tasks/ – Create task

GET /tasks/ – Get all tasks

🧪 Example Request
Create Project

POST /projects/

{
  "name": "Task Manager",
  "description": "Backend API Project"
}

🗄️ Database

PostgreSQL hosted on Render

Tables:

users

projects

tasks

Relationships:

One User → Many Projects

One Project → Many Tasks

⚙️ Environment Variables
DATABASE_URL=postgresql://<username>:<password>@<host>/<db_name>
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

🚀 Run Locally
git clone https://github.com/aadiiiitii001/Task-Project-Management-REST-API.git
cd task-management-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
