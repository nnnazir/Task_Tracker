"""
Таблица для БД Сотрудники
1. id - уникальный номер в БД.
2. email - электронный адрес, обязательный.
3. last_name - фамилия, обязательно.
4. first_name - имя, обязательно.
5. patronymic - отчество, необязательное.
6. post - должность, необязательное (?).
"""
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    patronymic = Column(String)
    post = Column(String)
    tasks = relationship('Task', back_populates='employees', lazy='joined')

    def __repr__(self):
        return (f"Employee(email='{self.email}', "
                f"last_name='{self.last_name}', "
                f"first_name='{self.first_name}', "
                f"patronymic='{self.patronymic}', "
                f"post='{self.post}')")

    def count_task(self) -> int:
        """
        Пробуем вернуть количество взятых для работы задач
        :return: количество задач
        """
        return len(self.tasks)