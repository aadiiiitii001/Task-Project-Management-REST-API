from app.db.base import Base
from app.db.session import engine
import app.models.user
import app.models.project
import app.models.task

def init_db_for_dev_only():
    Base.metadata.create_all(bind=engine)

