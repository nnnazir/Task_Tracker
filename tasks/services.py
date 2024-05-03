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
from employee.model import Employee
from employee.services import count_tasks
from tasks.model import Task
from tasks.schema import TasksList, TaskCreateUpdateSchema

api_task = APIRouter(tags=['Tasks'], prefix='/tasks')


@api_task.get('/', response_model=TasksList)
def get_tasks(db: Session = Depends(get_db),
              limit: int = 10, page: int = 1) -> dict:
    skip = (page - 1) * limit
    tasks = db.query(Task).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(tasks), 'tasks': tasks}


@api_task.get('/get/{taskId}')
def get_task(taskId: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == taskId).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Задание с id: {taskId} не найдено')
    return {"status": "success", "task": task}


@api_task.post('/create/', status_code=status.HTTP_201_CREATED)
def create_tasks(payload: TaskCreateUpdateSchema = Depends(),
                 db: Session = Depends(get_db)):
    new_task = Task(**payload.dict())
    if new_task.employee_id is not None and new_task.status == 0:
        new_task.status = 1
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {'status': 'success',
            'task': new_task}


@api_task.patch('/update/{taskId}')
def update_task(taskId: str, payload: TaskCreateUpdateSchema = Depends(),
                db: Session = Depends(get_db)):
    task_query = db.query(Task).filter(Task.id == taskId)
    task = task_query.first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Задание с id: {taskId} не найдено')
    update_data = payload.dict(exclude_unset=True)
    task_query.filter(Task.id == taskId).update(
        update_data, synchronize_session=False)
    db.commit()
    db.refresh(task)
    return {"status": "success", "task": task}


@api_task.delete('/del/{taskId}')
def delete_task(taskId: str, db: Session = Depends(get_db)):
    task_query = db.query(Task).filter(Task.id == taskId)
    task = task_query.first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Задание с id: {taskId} не найдено')
    task_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@api_task.get('/important')
def get_important_tasks(db: Session = Depends(get_db),
                        limit: int = 10, page: int = 1):
    """
    Получить важные задачи
    Читаем по статусу задачи = 0, потом проверяем есть ли родитель
    и взят ли родитель в работу
    :param db: указатель на БД
    :param limit: количество задач на страницу
    :param page: номер страницы
    :return: пока словарь: статус успешно, результат, список задач
    """
    skip = (page - 1) * limit
    tasks = (db.query(Task).filter(Task.status == 0).
             limit(limit).offset(skip).all())
    tasks_ret = []
    for task in tasks:
        if task.parent_id is not None and task.parent_task.status == 1:
            tasks_ret.append(task)

    return {'status': 'success', 'results': len(tasks_ret), 'tasks': tasks_ret}


@api_task.get('/free')
def get_free_tasks(db: Session = Depends(get_db),
                   limit: int = 10, page: int = 1):
    """
    Получить незадействованные задания
    Читаем по статусу задачи = 0
    :param db: указатель на БД
    :param limit: количество задач на страницу
    :param page: номер страницы
    :return: пока словарь: статус успешно, результат, список задач
    """
    skip = (page - 1) * limit
    tasks = (db.query(Task).filter(Task.status == 0).
             limit(limit).offset(skip).all())

    return {'status': 'success', 'results': len(tasks), 'tasks': tasks}


@api_task.patch('/set_employee/{taskId}')
def set_employee_important_task(taskId: str, db: Session = Depends(get_db)):
    """
    Для важной задачи установить исполнителя (?).
    1. Читаем данные по заданию.
    2. Ищем сотрудника, который может задачу
    (наименее загруженный сотрудник или сотрудник выполняющий
    родительскую задачу если ему назначено максимум на 2 задачи больше,
    чем у наименее загруженного сотрудника).
    3. Обновляем данные задания.
    :param taskId: ИД задания.
    :param db: Подключаемся к БД.
    :return: Вернуть обновленные данные по задаче (?).
    """
    task_query = db.query(Task).filter(Task.id == taskId)
    task = task_query.first()
    employee_parent = task.parent_task
    payload = TaskCreateUpdateSchema(
        name=task.name,
        content=task.content,
        period_of_execution=task.period_of_execution,
        parent_id=task.parent_id,
        status=task.status,
        employee_id=task.employee_id
    )

    # Получаем сотрудников, ищем свободного сотрудника, без задач
    employees_query = db.query(Employee).all()
    employees_query = sorted(employees_query, key=count_tasks)
    employee_min = employees_query[0]
    employees_free = []
    for employee in employees_query:
        if employee.count_task() == 0:
            employees_free.append(employee)
    employee_free = employee_min
    # Если свободный есть, берем первый и обновляем задание.
    if len(employees_free) > 0:
        employee_free = employees_free[0]
    else:
        # Если нет свободного, ищем с наименьшим количеством задач и сотрудника,
        # имеющего в работе родительскую задачу.
        if employee_parent.count_task() < employee_min.count_task() + 3:
            employee_free = employee_parent

    payload.employee_id = employee_free.id
    payload.status = 1
    update_data = payload.dict(exclude_unset=True)
    # Если нет, ищем дальше.
    task_query.filter(Task.id == taskId).update(
        update_data, synchronize_session=False)
    db.commit()
    db.refresh(task)
    return {"status": "success", "task": task}