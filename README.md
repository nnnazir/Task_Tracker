# SkyPro Дипломный проект
# TaskTracker

## Направление: 
backend

## Тэги:
Git, Readme, PEP8, Swagger, FastAPI, JSON, API

## Запуск на выполнение дипломного проекта

Используется Python 3.12
Описание работ для PyCharm в Windows.

1. Создать и активировать виртуальное окружение.
python -m venv venv
.\venv\Scripts\activate

2. Установить зависимости проекта, указанные в файле requirements.txt
pip install -r requirements.txt 
или средствами PyCharm.

3. Проверить наличие установленного PostgreSQL
4. 
4. Создать файл .env на основе sample.env

4. Запустить сервер
uvicorn main:app --reload 

При запуске отображается список сотрудников с принятыми задачами

localhost:8000/employees/ - список сотрудников.
localhost:8000/employees/busy - список занятых сотрудников и задания.
localhost:8000/employees/free - свободные сотрудники для задания?
localhost:8000/tasks/ - список заданий и работа с заданиями.
localhost:8000/tasks/important/ - список важных заданий.

5. Работать с базой данных или просматривать документацию API можно:
localhost:8000/docs или
localhost:8000/redoc

6. После первого запуска программы можно заполнить базу данных из скрипта 
tasktracker.sql. В этом файле только данные.