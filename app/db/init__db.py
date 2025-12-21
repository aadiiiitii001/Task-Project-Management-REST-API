from app.db.base import Base
from app.db.session import engine
from app.models import users,project,task

def init__db():
  Base.metadata.create_all(bind=engine)
