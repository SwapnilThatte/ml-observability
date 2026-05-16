import requests

FRAUD_SERVICE = "http://fraud-service:8001/predict"

def call_fraud_service(payload):

    return requests.post(FRAUD_SERVICE, json=payload).json()