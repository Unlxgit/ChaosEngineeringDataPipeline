from flask import Flask, render_template, request, jsonify, abort, redirect
from random import randint
import os
import sys
import json
import logging
import socket
import redis
import datetime

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger()
redis = redis.StrictRedis(host=os.getenv('REDIS'), port=6379, db=0)
app = Flask(__name__)
hostname = socket.getfqdn()

def lookup(key):
    if not os.getenv('REDIS'):
        return None
    try:
        value = int(redis.get(key))
        if not value:
            log.info(f"Redis lookup of key {key} failed. No data.")
            return None
        return value
    except Exception as ex:
        log.error(f"Redis lookup for {key} failed due to {ex}")
        return None

def cache(key, value):
    if not os.getenv('REDIS'):
        return None
    try:
        redis.set(key, value)
        return value
    except Exception as ex:
        log.error(f"Redis write for {key} failed due to {ex}")
        return None

@app.route("/prime/<number>")
def number(number):
    try:
        n = int(number)
        divisor = lookup(n)
        if divisor:
            return f"{ n } is not a prime number. It can be divided by {divisor} (answer from { hostname } via cache)"
        for i in range(2, (n // 2) + 1):
            if n % i == 0:
                cache(n, i)
                return f"{ n } is not a prime number. It can be divided by { i } (answer from { hostname }; processed)"
        return f"Yes! random { n } is a prime number (answer from { hostname } )."
    except Exception as ex:
        log.error(f"Exception: { ex }")
        abort(500, f"random { n } could not be processed (answer from { hostname }")

@app.route("/")
def ready():
    return "The prime app is ready and alive."

log.info(f"[{datetime.datetime.now()}] Starting prime number checker. My redis server is: {os.getenv('REDIS')}")
app.run(host='0.0.0.0', port=80)
