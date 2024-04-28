"""
Файл с сервисными функциями.
Пока реализовано:
Создание БД при ее отсутствии, используется psycopg2.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from src.config import DB_NAME, DB_USER, DB_PASS


def create_db():
    # Создание БД при ее отсутствии.
    # Устанавливаем соединение с postgres
    conn = psycopg2.connect(user=DB_USER, password=DB_PASS)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM pg_catalog.pg_database "
                    f"WHERE datname = '{DB_NAME}'")
        result = cur.fetchone()
        if result[0] == 0:
            cur.execute(f"CREATE DATABASE {DB_NAME};")
            conn.commit()
        # else:
        #     print("БД с таким названием уже существует.")
    cur.close()
    conn.close()
