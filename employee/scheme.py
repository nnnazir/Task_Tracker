"""
Файл со схемой Сотрудник
"""
from pydantic import BaseModel, EmailStr


class EmployeeSchema(BaseModel):
    """
    Схема Сотрудник.
    """
    id: str | None = None
    email: EmailStr
    last_name: str
    first_name: str
    patronymic: str | None = None
    post: str | None = None

    class Config:
        from_attributes = True
        population_by_name = True
        arbitrary_types_allowed = True
