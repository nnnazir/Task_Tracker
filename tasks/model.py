"""
Таблица для БД Задания
1. id - уникальный идентификатор в БД.
2. name - наименование задания, уникальное, обязательное.
3. content - содержание задания, обязательное.
4. period_of_execution - срок выполнения дата+время ?
5. parent_id - ссылка на родительскую задачу.
6. status - статус выполнения задачи, пока: 0 - ждет исполнителя, 1 - в работе
7. employee_id - ссылка на сотрудника, выполняющего задание
"""

import uuid
from sqlalchemy import (Column, Integer, String, Text, ForeignKey, TIMESTAMP)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from employee.model import Base


class Task(Base):
    __tablename__ = 'task'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    content = Column(Text, nullable=False)
    period_of_execution = Column(TIMESTAMP(timezone=True))
    parent_id = Column(UUID(as_uuid=True), ForeignKey('task.id'),
                       nullable=True)
    status = Column(Integer, nullable=False, default=0)
    employee_id = Column(UUID(as_uuid=True), ForeignKey('employee.id'),
                         nullable=True)
    employees = relationship(
        "Employee", back_populates='tasks', lazy='joined'
    )
    child_task = relationship(
        "Task", back_populates='parent_task', lazy='joined'
    )
    parent_task = relationship(
        "Task", remote_side='Task.id', back_populates='child_task',
        foreign_keys=[parent_id], lazy='joined'
    )

    def __repr__(self):
        return (f"Task(name='{self.name}', "
                f"content='{self.content}', "
                f"period_of_execution='{self.period_of_execution}', "
                f"parent_id='{self.parent_id}',"
                f"employee_id='{self.employee_id}',"
                f"status='{self.status}')")
