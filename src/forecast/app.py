import math
import time

import numpy as np
from flask import Flask, jsonify
import logging
import psycopg2
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

app = Flask(__name__)

DB_NAME = 'mydatabase'
DB_USER = 'myuser'
DB_PASSWORD = 'mypassword'
DB_HOST = 'postgres-service.gasai.svc.cluster.local'
DB_PORT = '5432'
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
        app.logger.error(f"Error connecting to database: {e}")
        return None


def get_current_data_point(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT price, time FROM price_history ORDER BY time DESC LIMIT 1")
        result = cursor.fetchone()
        return result


def get_data(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT time, price  FROM price_history ORDER BY time")
        result = cursor.fetchall()
        # create dataframe
        df = pd.DataFrame(result, columns=['time', 'price'])
        return df


def clean_data(df, current_minute):
    df['time'] = pd.to_datetime(df['time'])
    # check if most recent value is missing

    datetime_current_minute = pd.to_datetime(current_minute, unit='s')
    if df['time'].max() < datetime_current_minute:
        app.logger.info("Most recent value is missing")
        df = pd.concat([df, pd.DataFrame({'time': [datetime_current_minute], 'price': [None]})])
    df = df.drop_duplicates(subset='time', keep='last')
    df.set_index('time', inplace=True)
    full_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq='T')

    df = df.reindex(full_index)

    df['price'] = df['price'].ffill()
    return df


def build_response(time, latest, prediction):
    app.logger.info(f"Time: {time}, Latest: {latest}, Prediction: {prediction}")
    return jsonify({"time": time, "latest": latest, "prediction": prediction})


def get_train_data(df):
    X = []
    Y = []
    for i in range(5, len(df)):
        X.append(df.values[i - 5:i])
        Y.append(df.values[i])
    X = np.array(X).reshape(-1, 5)
    Y = np.array(Y).flatten()
    return X, Y


def get_forecast(train_x, train_y, current):
    # train model
    model = DecisionTreeRegressor()
    model.fit(train_x, train_y)
    # predict
    app.logger.info(f"Current: {current.shape}")
    prediction = model.predict([current])[0]
    return prediction


@app.route("/", methods=['GET'])
def get_hello():
    connection = connect_to_db()
    if connection is None:
        return "Error connecting to database", 500
    df = get_data(connection)
    df = df.dropna()
    if df.empty:
        return "No data found", 404
    current_minute = math.floor(time.time() / 60) * 60

    df = clean_data(df, current_minute)

    app.logger.info(f"Making predictions with {df.shape[0]} data points.")

    if df.shape[0] < 6:
        app.logger.info("Not enough data for prediction. Datapoints: ", df.shape[0])
        # not enough data for prediction -> answer with latest data point
        latest_price = df.values[-1][1]
        return build_response(current_minute, latest_price, latest_price)

    train_x, train_y = get_train_data(df)

    prediction = get_forecast(train_x, train_y, df['price'].values[-5:])

    latest_price = df['price'].values[-1]

    return build_response(current_minute, latest_price, prediction)

app.run(host='0.0.0.0', port=80)
