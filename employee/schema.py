"""
Файл со схемой Сотрудник
"""
from uuid import UUID
from typing import List
from pydantic import BaseModel, EmailStr


class BaseEmployeeSchema(BaseModel):
    """
    Базовая схема Сотрудник.
    Без uuid
    """
    email: EmailStr
    last_name: str
    first_name: str
    patronymic: str | None = None
    post: str | None = None

    class Config:
        from_attributes = True
        population_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "email": "example@test.com",
                "last_name": "Иванов",
                "first_name": "Иван",
                "patronymic": "Иванович",
                "post": "Инженер"
            }
        }


class EmployeeSchema(BaseEmployeeSchema):
    """
    Схема Сотрудник.
    Добавлен UUID
    """
    id: UUID


class EmployeeCreateUpdateSchema(BaseEmployeeSchema):
    """
    Схема Сотрудник для создания/обновления.
    """


class EmployeeList(BaseModel):
    """
    Список заданий
    """
    employees: List[EmployeeSchema]
