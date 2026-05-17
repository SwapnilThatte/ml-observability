import requests
from URL_DIR import FRAUD_SERVICE

FRAUD_SERVICE = f"{FRAUD_SERVICE}/predict"

def call_fraud_service(payload):

    return requests.post(FRAUD_SERVICE, json=payload).json()