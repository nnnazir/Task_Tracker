"""
Таблица для БД Сотрудники
1. id - уникальный номер в БД.
2. email - адрес, обязательный.
3. last_name - фамилия, обязательно.
4. first_name - имя, обязательно.
5. patronymic - отчество, необязательное.
6. post - должность, необязательное (?).
"""
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): pass


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(GUID, primary_key=True,
                server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    email = Column(String(40), nullable=False, unique=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    patronymic = Column(String(50))
    post = Column(String(50))
