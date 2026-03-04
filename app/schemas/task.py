from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TaskResponse(BaseModel):
    """
    Модель для создания задачи
    """
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True) # если на вход придёт модель ORM

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = None
    is_completed:  Optional[bool] = None