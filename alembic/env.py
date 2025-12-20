from app.db.base import Base
from app.db.session import engine

# import all models so Alembic can detect them
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
