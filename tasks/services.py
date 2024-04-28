"""
Файл с сервисными функциями по Заданиям.
Пробуем реализовать CRUD.
1. Получение данных по всем заданиям.
2. Добавление нового задания.
3. Редактирование данных о задании.
4. Удаление данных задания.
5. Чтение данных об одном задании
"""

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session

from src.db import get_db
from tasks.model import Task
from tasks.scheme import TaskSchema

api_task = APIRouter()


@api_task.get('/')
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return {'status': 'success', 'results': len(tasks), 'tasks': tasks}


@api_task.post('/', status_code=status.HTTP_201_CREATED)
def create_tasks(payload: TaskSchema = Depends(),
                     db: Session = Depends(get_db)):
    new_task = Task(**payload.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {'status': 'success',
            'task': new_task}


@api_task.patch('/{taskId}')
def update_task(taskId: str, payload: TaskSchema = Depends(),
                    db: Session = Depends(get_db)):
    task_query = db.query(Task).filter(Task.id == taskId)
    db_task = task_query.first()
    
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Задание с id: {taskId} не найдено')
    update_data = payload.dict(exclude_unset=True)
    task_query.filter(Task.id == taskId).update(
        update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_task)
    return {"status": "success", "task": db_task}


@api_task.get('/{taskId}')
def get_task(taskId: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == taskId).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Задание с id: {taskId} не найдено')
    return {"status": "success", "task": task}


@api_task.delete('/{taskId}')
def delete_task(taskId: str, db: Session = Depends(get_db)):
    task_query = db.query(Task).filter(Task.id == taskId)
    task = task_query.first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Задание с id: {taskId} не найдено')
    task_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
