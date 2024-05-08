from flask import Flask
import requests
import redis
import os
import logging
import datetime

app = Flask(__name__)
redis = redis.StrictRedis(host=os.getenv('REDIS'), port=6379, db=0)

logging.basicConfig(level=logging.INFO)


def lookup(key):
    if not os.getenv('REDIS'):
        return None
    try:
        value = int(redis.get(key))
        if not value:
            app.logger.info(f"Redis lookup of key {key} failed. No data.")
            return None
        return value
    except Exception as ex:
        app.logger.error(f"Redis lookup for {key} failed due to {ex}")
        return None


def cache(key, value):
    if not os.getenv('REDIS'):
        return None
    try:
        redis.set(key, value)
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
            return f"The response was looked up and is {lookup_response}"

        response = requests.get(prime_service_url + endpoint)
        if response.status_code == 200:
            cache(current_time_stamp, response.json())
            return response.json()
        else:
            return {"error": "Failed to retrieve prime info"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


app.run(host='0.0.0.0', port=80)
