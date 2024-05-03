"""
Файл с сервисными функциями по Сотрудникам.
Пробуем реализовать CRUD.
1. Получение данных по всем сотрудникам.
2. Добавление нового сотрудника.
3. Редактирование данных о сотруднике.
4. Удаление данных сотрудника.
5. Чтение данных об одном сотруднике
"""

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session, joinedload

from src.db import get_db
from employee.model import Employee
from employee.schema import (EmployeeList, EmployeeCreateUpdateSchema)

api_employee = APIRouter(tags=['Employees'], prefix='/employees')


def count_tasks(s):
    return len(s.tasks)


@api_employee.get('/', response_model=EmployeeList)
def get_employees(db: Session = Depends(get_db)) -> dict:
    employees = db.query(Employee).all()
    print(employees)
    return {'status': 'success',
            'results': len(employees),
            'employees': employees}


@api_employee.get('/get/{employeeId}')
def get_employee(employeeId: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employeeId).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Сотрудник с id: {employeeId} не найден")
    return {"status": "success", "employee": employee}


@api_employee.post('/create', status_code=status.HTTP_201_CREATED)
def create_employees(payload: EmployeeCreateUpdateSchema = Depends(),
                     db: Session = Depends(get_db)):
    new_employee = Employee(**payload.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return {'status': 'success', 'employee': new_employee}


@api_employee.patch('/update/{employeeId}')
def update_employee(employeeId: str,
                    payload: EmployeeCreateUpdateSchema = Depends(),
                    db: Session = Depends(get_db)):
    employee_query = db.query(Employee).filter(Employee.id == employeeId)
    db_employee = employee_query.first()

    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Сотрудник с id: {employeeId} не найден')
    update_data = payload.dict(exclude_unset=True)
    employee_query.filter(Employee.id == employeeId).update(
        update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_employee)
    return {"status": "success", "employee": db_employee}


@api_employee.delete('/del/{employeeId}')
def delete_employee(employeeId: str, db: Session = Depends(get_db)):
    employee_query = db.query(Employee).filter(Employee.id == employeeId)
    employee = employee_query.first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Сотрудник с id: {employeeId} не найден')
    employee_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@api_employee.get('/busy', response_model=EmployeeList)
def get_employees_busy(db: Session = Depends(get_db)) -> dict:
    employees_query = (db.query(Employee).options(joinedload(Employee.tasks)).
                       filter(Employee.tasks is not None).all())
    employees = []
    for employee in employees_query:
        if len(employee.tasks) != 0:
            employees.append(employee)
    employees = sorted(employees, key=count_tasks, reverse=True)

    return {'status': 'success',
            'results': len(employees),
            'employees': employees}


@api_employee.get('/free')
def get_employees_free(db: Session = Depends(get_db)):
    """
    Пытаемся получить свободных сотрудников.
    :param db:
    :return: Пока словарь со свободными сотрудниками.
    """

    employees_query = db.query(Employee).all()
    employees = []
    for employee in employees_query:
        if len(employee.tasks) == 0:
            employees.append(employee)

    if len(employees) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Сотрудников без заданий не найдено')

    return {"status": "success", "employees": employees}