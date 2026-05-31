from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.utils.dependencies import get_current_user, require_role

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    return db.query(User).all()
