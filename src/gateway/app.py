from flask import Flask
import requests
app = Flask(__name__)

@app.route("/")
def get_prime_info():
    prime_service_url = "http://forecast-service.gasai.svc.cluster.local"  # Kubernetes service DNS
    endpoint = "/"  # Assuming this endpoint exists in prime-service

    try:
        response = requests.get(prime_service_url + endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to retrieve prime info"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

app.run(host='0.0.0.0', port=80)
