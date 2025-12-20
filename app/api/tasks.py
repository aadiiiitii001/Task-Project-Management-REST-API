from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse
from app.utils.dependencies import get_current_user, require_role
from app.utils.pagination import get_pagination

router = APIRouter()

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("manager"))],
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        project_id=task.project_id,
        assigned_to=task.assigned_to,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    pagination=Depends(get_pagination),
):
    offset, limit = pagination

    query = db.query(Task)

    # Users can only see their own tasks
    if current_user.role == "user":
        query = query.filter(Task.assigned_to == current_user.id)

    tasks = query.offset(offset).limit(limit).all()
    return tasks


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Regular users can update only their own tasks
    if current_user.role == "user" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    task.status = status
    db.commit()
    db.refresh(task)
    return task
