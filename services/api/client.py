# import requests
# from URL_DIR import FRAUD_SERVICE

# FRAUD_SERVICE = f"{FRAUD_SERVICE}/predict"

# def call_fraud_service(payload):

#     return requests.post(FRAUD_SERVICE, json=payload).json()

import os
import httpx

FRAUD_SERVICE_URL = os.getenv(
    "FRAUD_SERVICE_URL",
    "http://fraud-service:8001/predict"
)


async def call_fraud_service(payload):

    async with httpx.AsyncClient() as client:

        response = await client.post(
            FRAUD_SERVICE_URL,
            json=payload,
            timeout=5.0
        )

        return response.json()