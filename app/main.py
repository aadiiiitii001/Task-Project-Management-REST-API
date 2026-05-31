import os
from fastapi import FastAPI
from app.api import auth, users, projects, tasks

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    description="REST API for managing users, projects, and tasks with JWT auth and role-based access control.",
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Task Management API is running"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
