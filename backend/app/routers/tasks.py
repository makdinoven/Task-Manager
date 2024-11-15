from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..dependencies import get_db, get_current_user

router = APIRouter()

# Создание новой задачи
@router.post("/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_task(db=db, task=task, user_id=current_user.id)

# Редактирование задачи (всех полей)
@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_task = crud.get_task(db, task_id=task_id, user_id=current_user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db=db, db_task=db_task, task=task)

# Смена статуса задачи на "В процессе"
@router.put("/{task_id}/start", response_model=schemas.Task)
def start_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_task = crud.get_task(db, task_id=task_id, user_id=current_user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task_status(db=db, db_task=db_task, status=schemas.TaskStatus.IN_PROGRESS)

# Смена статуса задачи на "Готово"
@router.put("/{task_id}/complete", response_model=schemas.Task)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_task = crud.get_task(db, task_id=task_id, user_id=current_user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task_status(db=db, db_task=db_task, status=schemas.TaskStatus.COMPLETED)

# Удаление задачи
@router.delete("/{task_id}", response_model=dict)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_task = crud.get_task(db, task_id=task_id, user_id=current_user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db=db, db_task=db_task)
    return {"message": "Task deleted successfully"}

# Смена приоритета задачи
@router.put("/{task_id}/priority", response_model=schemas.Task)
def update_task_priority(
    task_id: int,
    priority: schemas.TaskPriority,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_task = crud.get_task(db, task_id=task_id, user_id=current_user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task_priority(db=db, db_task=db_task, priority=priority)
