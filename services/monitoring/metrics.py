import pandas as pd
import numpy as np
from dashboard import BUFFER


# =========================================================
# COMPUTE LIVE METRICS
# =========================================================

def compute_metrics():

    if len(BUFFER) == 0:

        return {
            "status": "no_data"
        }

    df = pd.DataFrame(list(BUFFER))

    try:

        df["probability"] = (
            df["probability"].astype(float)
        )

        df["latency_ms"] = (
            df["latency_ms"].astype(float)
        )

    except Exception:

        return {
            "status": "invalid_data"
        }

    total_requests = len(df)

    fraud_rate = (
        df["decision"] == "BLOCK"
    ).mean()

    review_rate = (
        df["decision"] == "REVIEW"
    ).mean()

    allow_rate = (
        df["decision"] == "ALLOW"
    ).mean()

    return {

        "status": "healthy",

        "total_requests": int(total_requests),

        "avg_latency_ms": round(
            float(df["latency_ms"].mean()),
            2
        ),

        "p95_latency_ms": round(
            float(
                np.percentile(
                    df["latency_ms"],
                    95
                )
            ),
            2
        ),

        "max_latency_ms": round(
            float(df["latency_ms"].max()),
            2
        ),

        "fraud_rate": round(
            float(fraud_rate),
            4
        ),

        "review_rate": round(
            float(review_rate),
            4
        ),

        "allow_rate": round(
            float(allow_rate),
            4
        ),

        "avg_probability": round(
            float(df["probability"].mean()),
            4
        )
    }