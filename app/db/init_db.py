from app.db.base import Base
from app.db.session import engine
import app.db.base_class  # noqa

def init_db_for_dev_only():
    Base.metadata.create_all(bind=engine)
