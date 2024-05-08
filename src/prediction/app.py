from flask import Flask
app = Flask(__name__)

@app.route("/")
def ready():
    # log that requested
    print("Hello world.")
    return "Hello world."

app.run(host='0.0.0.0', port=80)
