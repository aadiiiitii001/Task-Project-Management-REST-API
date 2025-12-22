from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.utils.dependencies import require_role

router = APIRouter()


@router.get(
    "/",
    response_model=list[UserResponse],
    dependencies=[Depends(require_role("admin"))],
)
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()
