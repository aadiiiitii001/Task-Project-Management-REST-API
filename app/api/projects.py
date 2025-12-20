from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse
from app.utils.dependencies import require_role

router = APIRouter()

@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
):
    new_project = Project(
        name=project.name,
        description=project.description,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()
