"""
Файл с моделью данных Задание
"""
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class TaskSchema(BaseModel):
    id : str | None = None
    name: str
    content: str
    period_of_execution: datetime | None = None
    parent_id: str | None = None
    status: int = 0
    employee_id: str | None = None

    class Config:
        from_attributes = True
        population_by_name = True
        arbitrary_types_allowed = True
