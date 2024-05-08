from flask import Flask
import requests
import redis
import os
import logging
import datetime

app = Flask(__name__)

# Initialize Redis connection using the DNS name of the redis-service
redis_host = os.getenv('REDIS_HOST', 'redis-service.gasai.svc.cluster.local')
redis_port = 6379
redis_password = None  # Set this if your Redis service requires authentication

# Create a Redis client
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)

logging.basicConfig(level=logging.INFO)


def lookup(key):
    try:
        value = redis_client.get(key)
        if value:
            app.logger.info(f"Redis lookup of key {key} succeeded.")
            return value.decode()  # Decode the byte value to string
        else:
            app.logger.info(f"Redis lookup of key {key} failed. No data.")
            return None
    except Exception as ex:
        app.logger.error(f"Redis lookup for {key} failed due to {ex}")
        return None


def cache(key, value):
    try:
        redis_client.set(key, value)
        app.logger.info(f"Successfully cached value for key {key}.")
        return value
    except Exception as ex:
        app.logger.error(f"Redis write for {key} failed due to {ex}")
        return None


@app.route("/")
def get_prime_info():
    prime_service_url = "http://forecast-service.gasai.svc.cluster.local"
    endpoint = "/"
    current_time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        lookup_response = lookup(current_time_stamp)
        if lookup_response:
            return f"The response was looked up and is {lookup_response} at {current_time_stamp}"

        response = requests.get(prime_service_url + endpoint)
        if response.status_code == 200:
            prime_info = response.json()
            cache(current_time_stamp, str(prime_info))  # Cache the response as a string
            return str(prime_info) + current_time_stamp
        else:
            return {"error": "Failed to retrieve prime info"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
