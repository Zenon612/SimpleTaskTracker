from typing import Any, Sequence
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.task import TaskResponse
from app.models.task import TaskModel
from app.core.db import get_db


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskResponse, db: AsyncSession = Depends(get_db)) -> TaskModel:
    task_data= task.model_dump()
    db_task = TaskModel(**task_data)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

@router.get("/", response_model=list[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_db)) -> Sequence[Any]:
    query = select(TaskModel)
    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession= Depends(get_db)): # если будет не int - вернёт 422
    task = await db.get(TaskModel, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}") # не добавлял response model, так как pydantic не пропустит ответ
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.get(TaskModel, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    return {"message": f"task{task_id} deleted successfully"}
