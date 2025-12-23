from app.db.base import Base
from app.db.session import engine
from app.models import users, project, task

def init_db_for_dev_only():
    Base.metadata.create_all(bind=engine)
