import time
import logging
import os
import psycopg2

# Database connection parameters
DB_NAME = 'mydatabase'
DB_USER = 'myuser'
DB_PASSWORD = 'mypassword'
DB_HOST = 'postgres-service.gasai.svc.cluster.local'
DB_PORT = '5432'
logger = logging.getLogger()

logging.basicConfig(level=logging.INFO)

def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return connection
    except psycopg2.OperationalError as e:
        print(f"Error connecting to database: {e}")
        return None


def create_table_if_not_exists(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS numbers (
                id SERIAL PRIMARY KEY,
                number INTEGER NOT NULL
            );
        """)
        connection.commit()
        logging.info("Created table 'numbers' if it did not exist")

def insert_number(connection, number):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO numbers (number) VALUES (%s)", (number,))
        connection.commit()
        logger.info(f"Inserted number: {number}")




def main():
    connection = None
    while connection is None:
        connection = connect_to_db()
        if connection is None:
            logger.info("Retrying database connection in 5 seconds")
            time.sleep(5)
    create_table_if_not_exists(connection)
    number = 1
    while True:
        insert_number(connection, number)
        number += 1
        time.sleep(60)

if __name__ == '__main__':
    main()