import os
from fastapi import FastAPI
from app.api import auth, users, projects, tasks
from alembic.config import Config
from alembic import command

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    description="REST API for managing users, projects, and tasks with JWT auth and role-based access control.",
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

run_migrations()

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Task Management API is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
