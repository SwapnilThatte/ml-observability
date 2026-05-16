from fastapi import FastAPI
from model import FraudModel
from preprocessing import preprocess
from schemas import Transaction
from config import *

app = FastAPI(title="Fraud Service")

model = FraudModel("../../models/xgboost_model.json")


@app.post("/predict")
def predict(tx: Transaction):

    X = preprocess(tx.dict())

    prob = model.predict_proba(X)[0][1]

    if prob > THRESHOLD_BLOCK:
        decision = "BLOCK"
    elif prob > THRESHOLD_REVIEW:
        decision = "REVIEW"
    else:
        decision = "ALLOW"

    return {
        "fraud_probability": float(prob),
        "decision": decision
    }