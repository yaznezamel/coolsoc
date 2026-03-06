import psycopg2
from psycopg2.extras import RealDictCursor

try:
    conn = psycopg2.connect(
        host='localhost',
        database='fastapi',
        user='postgres',
        password='Azure@admin4',
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("Successfully connected to the database")
except Exception as error:
    print(error)
