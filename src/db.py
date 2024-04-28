from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from databases import Database

from src.config import DB_NAME, DB_USER, DB_PASS

DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
