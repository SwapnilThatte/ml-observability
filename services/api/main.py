import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from client import call_fraud_service
from schemas import Transaction

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

logger = logging.getLogger("api-gateway")


# =========================================================
# APPLICATION LIFECYCLE
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting API Gateway...")

    yield

    logger.info("Shutting down API Gateway...")


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Fraud Detection API Gateway",
    description=(
        "API Gateway for real-time "
        "credit card fraud detection."
    ),
    version="1.0.0",
    lifespan=lifespan
)


# =========================================================
# MIDDLEWARE
# REQUEST LATENCY TRACKING
# =========================================================

@app.middleware("http")
async def add_process_time_header(
    request: Request,
    call_next
):

    start_time = time.time()

    response = await call_next(request)

    process_time = (
        time.time() - start_time
    ) * 1000

    response.headers[
        "X-Process-Time-MS"
    ] = str(round(process_time, 2))

    logger.info(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{process_time:.2f}ms"
    )

    return response


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
async def home():

    return {
        "status": "success",
        "service": "API Gateway",
        "message": (
            "Fraud Detection Gateway Running"
        )
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }


# =========================================================
# MAIN TRANSACTION ENDPOINT
# =========================================================

@app.post("/transaction")
async def transaction(tx: Transaction):

    try:

        logger.info(
            "Received transaction request"
        )

        response = await call_fraud_service(
            tx.data
        )

        logger.info(
            "Fraud service response received"
        )

        return {
            "status": "success",
            "prediction": response
        }

    except HTTPException as e:

        logger.exception(
            "HTTP exception occurred"
        )

        raise e

    except Exception as e:

        logger.exception(
            "Unhandled exception"
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
        f"Unhandled error: {str(exc)}"
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
        port=8000,
        reload=True
    )
    
# from fastapi import FastAPI
# from client import call_fraud_service
# from schemas import Transaction
# import uvicorn

# app = FastAPI(title="API Gateway")


# @app.post("/transaction")
# async def transaction(tx: Transaction):

#     return call_fraud_service(tx.data)

# @app.get("/")
# async def home():
#     return {"status" : "success", "message" : "Hello World"}


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
