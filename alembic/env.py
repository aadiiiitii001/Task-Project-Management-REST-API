from app.db.base import Base
from app.db.session import engine

# IMPORTANT: import all models
from app.models import user, project, task

target_metadata = Base.metadata
