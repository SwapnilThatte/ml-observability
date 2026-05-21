import time
import threading
import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from dashboard import fetch_stream_events
from metrics import compute_metrics

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
    "monitoring-service"
)


# =========================================================
# SHARED LIVE METRICS
# =========================================================

latest_metrics = {
    "status": "starting"
}


# =========================================================
# BACKGROUND WORKER
# =========================================================

def metrics_worker():

    global latest_metrics

    logger.info(
        "Metrics worker started"
    )

    while True:

        try:

            fetch_stream_events()

            latest_metrics = (
                compute_metrics()
            )

        except Exception as e:

            logger.exception(
                "Metrics worker failure"
            )

        time.sleep(1)


# =========================================================
# APP LIFECYCLE
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        "Starting Monitoring Service"
    )

    thread = threading.Thread(
        target=metrics_worker,
        daemon=True
    )

    thread.start()

    yield

    logger.info(
        "Stopping Monitoring Service"
    )


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Monitoring Service",
    version="1.0.0",
    lifespan=lifespan
)


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
async def home():

    return {
        "status": "success",
        "service": "Monitoring Service"
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
# LIVE DASHBOARD
# =========================================================

@app.get("/dashboard")
async def dashboard():

    return JSONResponse(
        content=latest_metrics
    )


# =========================================================
# RAW EVENT BUFFER
# =========================================================

@app.get("/events")
async def events():

    from dashboard import BUFFER

    return {
        "total_events": len(BUFFER),
        "events": list(BUFFER)[-50:]
    }


# =========================================================
# UVICORN ENTRYPOINT
# =========================================================

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8002,
        reload=True
    )