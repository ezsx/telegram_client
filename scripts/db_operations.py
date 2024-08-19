import os
import psycopg2
from psycopg2.extras import execute_values


def insert_messages_to_db(messages):
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO news (published_at, text, embedding) 
    VALUES %s
    """

    data = [(msg[1], msg[2], msg[3]) for msg in messages]
    execute_values(cursor, insert_query, data)

    conn.commit()
    cursor.close()
    conn.close()
