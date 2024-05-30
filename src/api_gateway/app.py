from flask import Flask, jsonify
import requests
import redis
import os
import logging
import datetime
from retry import retry
import psycopg2


app = Flask(__name__)

# Initialize Redis connection using the DNS name of the redis-service
redis_host = os.getenv('REDIS_HOST', 'redis-service.gasai.svc.cluster.local')
redis_port = 6379
redis_password = None  # Set this if your Redis service requires authentication

# Create a Redis client
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)

logging.basicConfig(level=logging.INFO)


DB_NAME = 'mydatabase'
DB_USER = 'myuser'
DB_PASSWORD = 'mypassword'
DB_HOST = 'postgres-service.gasai.svc.cluster.local'
DB_PORT = '5432'
logging.basicConfig(level=logging.INFO)


@retry(tries=4, delay=0.05)
def connect_to_db():
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return connection

@retry(tries=4, delay=0.05)
def get_one_data_point(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT price, time FROM price_history ORDER BY time DESC LIMIT 1")
        result = cursor.fetchone()
        return result


def lookup(key):
    @retry(tries=4, delay=0.05)
    def inner_lookup(key):
        value = redis_client.get(key)
        if value:
            app.logger.info(f"Redis lookup of key {key} succeeded.")
            return value.decode()  # Decode the byte value to string
        else:
            app.logger.info(f"Redis lookup of key {key} failed. No data.")
            return None

    try:
        return inner_lookup(key)
    except Exception as e:
        app.logger.error(f"Redis not available: {str(e)}")
        return None


def cache(key, value):
    @retry(tries=4, delay=0.05)
    def inner_cache(key, value):
        redis_client.set(key, value)
        app.logger.info(f"Successfully cached value for key {key}")

    try:
        inner_cache(key, value)
    except Exception as e:
        app.logger.error(f"Failed to cache value: {str(e)}")


def get_forecast():
    @retry(tries=4, delay=0.05)
    def inner_get_forecast():
        prime_service_url = "http://forecast-service.gasai.svc.cluster.local"
        endpoint = "/forecast"
        response = requests.get(prime_service_url + endpoint)
        if response.status_code == 200:
            return response

        app.logger.error(f"Failed to retrieve forecast from forecast-service. Status code: {response.status_code}")
        raise requests.exceptions.RequestException("Failed to retrieve forecast from forecast-service.")

    try:
        return inner_get_forecast()
    except requests.exceptions.RequestException as e:
        prime_service_url = "http://forecast-service.gasai.svc.cluster.local"
        endpoint = "/forecast"
        return requests.get(prime_service_url + endpoint)


@app.route('/health')
def health():
    return jsonify(status="ok"), 200


@app.route('/ready')
def ready():
    if connect_to_db() is None:
        return jsonify(status="error"), 500
    return jsonify(status="ok"), 200


@app.route("/forecast", methods=['GET'])
def forecast():
    current_time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    lookup_response = lookup(current_time_stamp)
    if lookup_response:
        return jsonify(eval(lookup_response)), 200

    try:
        response = get_forecast()

        if response.status_code == 200:
            price_info = response.json()
            cache(current_time_stamp, str(price_info))
            return jsonify(price_info), 200

        elif response.status_code == 500 and "database" in response.json().get('error'):
            return jsonify({"error": "Service unavailable"}), 500
        else:
            connection = connect_to_db()
            latest = get_one_data_point(connection)
            return jsonify({"time": current_time_stamp, "latest": latest[0], "prediction": latest[0]}), 200


    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Service unavailable"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
