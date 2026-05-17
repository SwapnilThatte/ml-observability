from fastapi import FastAPI
from model import FraudModel
from preprocessing import preprocess
from schemas import Transaction
from config import *
import uvicorn

app = FastAPI(title="Fraud Service")

model = FraudModel("xgboost_fraud_model.json")


@app.post("/predict")
async def predict(tx: Transaction):

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


@app.get("/")
async def home():
    return {"status" : "success", "message" : "Hello World from Fraud Detection Service !"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
