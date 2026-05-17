from fastapi import FastAPI
from client import call_fraud_service
from schemas import Transaction
import uvicorn

app = FastAPI(title="API Gateway")


@app.post("/transaction")
async def transaction(tx: Transaction):

    return call_fraud_service(tx.data)

@app.get("/")
async def home():
    return {"status" : "success", "message" : "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
