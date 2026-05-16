from fastapi import FastAPI
from client import call_fraud_service
from schemas import Transaction

app = FastAPI(title="API Gateway")


@app.post("/transaction")
def transaction(tx: Transaction):

    return call_fraud_service(tx.data)