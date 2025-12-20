from app.db.base import Base
from app.db.session import engine

# IMPORTANT: import models so Alembic can detect them
from app.models import user, project, task
