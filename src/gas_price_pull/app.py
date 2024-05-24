import random
import time
import logging
import os
import psycopg2
import math

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
            CREATE TABLE IF NOT EXISTS price_history (
                id SERIAL PRIMARY KEY,
                price DOUBLE PRECISION,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        logging.info("Created table 'numbers' if it did not exist")

def insert_price(connection, price, time):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO price_history (price, time) VALUES (%s, %s)
        """, (price, time))
        connection.commit()
        logger.info(f"Inserted price: {price} with time: {time}")


# one cycle per 20 minutes
def time_to_sin(current_time):
    T = 1200
    sin_measure = math.sin((2 * math.pi / T) * current_time)
    return sin_measure

def main():
    connection = None
    while connection is None:
        connection = connect_to_db()
        if connection is None:
            logger.info("Retrying database connection in 5 seconds")
            time.sleep(5)
    create_table_if_not_exists(connection)

    while True:
        current_time = time.time()
        current_price = time_to_sin(current_time)
        if random.random() > 0.5:
            time_to_go_of = math.floor(current_time/60) * 60
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_to_go_of))
            insert_price(connection, current_price, timestamp)
        # Sleep until the next full minute
        time_of_next_full_minute = math.ceil(time.time() / 60) * 60
        # 0.001 seconds to make sure we are in the next minute
        time_until_next_full_minute = time_of_next_full_minute - time.time() + 0.001
        time.sleep(time_until_next_full_minute)


if __name__ == '__main__':
    main()