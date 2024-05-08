from flask import Flask, jsonify
import logging


app = Flask(__name__)

sample_data = {
    "message": "Hello world!"
}

logging.basicConfig(level=logging.INFO)
@app.route("/", methods=['GET'])
def get_hello():

    app.logger.info("Received GET request for /")

    # Return a JSON response containing the message
    return jsonify(sample_data)

app.run(host='0.0.0.0', port=80)
