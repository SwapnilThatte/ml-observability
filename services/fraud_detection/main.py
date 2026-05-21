import time
import logging

from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    HTTPException,
    Request
)

from fastapi.responses import JSONResponse

from model import FraudModel
from preprocessing import preprocess
from schemas import (
    Transaction,
    PredictionResponse
)

from config import (
    THRESHOLD_BLOCK,
    THRESHOLD_REVIEW
)

from redis_client import redis_client

import uvicorn


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )
)

logger = logging.getLogger(
    "fraud-service"
)


# =========================================================
# LOAD MODEL
# =========================================================

MODEL_PATH = "/models/xgboost_fraud_model.json"

model = FraudModel(MODEL_PATH)


# =========================================================
# APP LIFECYCLE
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        "Starting Fraud Detection Service"
    )

    yield

    logger.info(
        "Stopping Fraud Detection Service"
    )


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Fraud Detection Service",
    version="1.0.0",
    lifespan=lifespan
)


# =========================================================
# LATENCY MIDDLEWARE
# =========================================================

@app.middleware("http")
async def latency_middleware(
    request: Request,
    call_next
):

    start = time.time()

    response = await call_next(request)

    latency_ms = (
        time.time() - start
    ) * 1000

    response.headers[
        "X-Latency-MS"
    ] = str(round(latency_ms, 2))

    return response


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
async def home():

    return {
        "status": "success",
        "service": (
            "Fraud Detection Service"
        )
    }


# =========================================================
# HEALTH ENDPOINT
# =========================================================

@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }


# =========================================================
# PREDICTION ENDPOINT
# =========================================================

@app.post(
    "/predict",
    response_model=PredictionResponse
)
async def predict(tx: Transaction):

    start = time.time()

    try:

        X = preprocess(tx.data)

        prob = float(
            model.predict_proba(X)[0][1]
        )

        if prob > THRESHOLD_BLOCK:

            decision = "BLOCK"

        elif prob > THRESHOLD_REVIEW:

            decision = "REVIEW"

        else:

            decision = "ALLOW"

        latency_ms = (
            time.time() - start
        ) * 1000

        logger.info(
            f"Prediction complete | "
            f"prob={prob:.4f} | "
            f"decision={decision} | "
            f"latency={latency_ms:.2f}ms"
        )

        # =================================================
        # STREAM EVENT TO REDIS
        # =================================================

        event = {

            "probability": str(prob),

            "decision": decision,

            "latency_ms": str(
                round(latency_ms, 2)
            ),

            "timestamp": str(
                time.time()
            )
        }

        redis_client.xadd(
            "fraud_events",
            event
        )

        return {
            "fraud_probability": prob,
            "decision": decision
        }

    except ValueError as e:

        logger.exception(
            "Validation error"
        )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        logger.exception(
            "Prediction failed"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GLOBAL EXCEPTION HANDLER
# =========================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(
        f"Unhandled exception: {str(exc)}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": (
                "Internal Server Error"
            )
        }
    )


# =========================================================
# UVICORN ENTRYPOINT
# =========================================================

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )

    
# from fastapi import FastAPI
# from model import FraudModel
# from preprocessing import preprocess
# from schemas import Transaction
# from config import *
# import uvicorn

# app = FastAPI(title="Fraud Service")

# model = FraudModel("xgboost_fraud_model.json")


# @app.post("/predict")
# async def predict(tx: Transaction):

#     X = preprocess(tx.dict())

#     prob = model.predict_proba(X)[0][1]

#     if prob > THRESHOLD_BLOCK:
#         decision = "BLOCK"
#     elif prob > THRESHOLD_REVIEW:
#         decision = "REVIEW"
#     else:
#         decision = "ALLOW"

#     return {
#         "fraud_probability": float(prob),
#         "decision": decision
#     }


# @app.get("/")
# async def home():
#     return {"status" : "success", "message" : "Hello World from Fraud Detection Service !"}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
