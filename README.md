    SkyPro Дипломный проект

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

4. Запустить сервер
uvicorn main:app --reload 

localhost:8000/employee/ - список сотрудников
localhost:8000/task/ - список заданий
Работать с базой данных можно используя docs или redoc:
localhost:8000/docs или
localhost:8000/redoc