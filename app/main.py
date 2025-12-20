import os
from fastapi import FastAPI
from app.api import auth, users, projects, tasks

# Create FastAPI instance
app = FastAPI(title="Task Management API")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

# Optional: Root endpoint for quick check
@app.get("/")
def root():
    return {"message": "Task Management API is running!"}

# For local development
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Use $PORT on Render
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
