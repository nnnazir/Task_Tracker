import uvicorn
from fastapi import FastAPI

from src.config import DB_HOST
from src.services import create_db
from src.db import engine

from employee.model import Base
from employee.services import api_employee

from tasks.services import api_task


create_db()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_employee, tags=['Employees'], prefix='/employees')
app.include_router(api_task, tags=['Tasks'], prefix='/tasks')

@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host=DB_HOST, port=8000)
