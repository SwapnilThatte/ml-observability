from pydantic import BaseModel


class DashboardResponse(BaseModel):

    status: str

    total_requests: int | None = None

    avg_latency_ms: float | None = None

    p95_latency_ms: float | None = None

    max_latency_ms: float | None = None

    fraud_rate: float | None = None

    review_rate: float | None = None

    allow_rate: float | None = None

    avg_probability: float | None = None