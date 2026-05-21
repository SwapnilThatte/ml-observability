# Real-Time ML based Financial Fraud Detection Pipeline & ML Observability
Designed to simulate realistic fintech-grade ML infrastructure with:
- low-latency inference
- concurrent request handling
- drift monitoring
- observability
- synthetic fraud simulation
- stress testing
- microservice isolation

---

# Architecture

```text
                +------------------+
                |    Locust Load   |
                |      Testing     |
                +---------+--------+
                          |
                          v
                +------------------+
                |   API Gateway    |
                |    FastAPI       |
                +---------+--------+
                          |
                          v
                +------------------+
                |  Fraud Service   |
                |    XGBoost       |
                +---------+--------+
                          |
                          v
                +------------------+
                |      Redis       |
                |  Event Streams   |
                +---------+--------+
                          |
                          v
                +------------------+
                | Monitoring Layer |
                |  Metrics + Drift |
                +------------------+
```

---

# Features

## ML System
- XGBoost fraud detection model
- High recall optimization
- SHAP explainability
- Drift-aware architecture
- Real-time inference
- Fraud thresholding system
- Adversarial anomaly testing

---

## Infrastructure
- FastAPI microservices
- Docker Compose deployment
- Redis Streams event pipeline
- Async inter-service communication
- Structured logging
- Health endpoints
- Latency tracking middleware

---

## Monitoring
- Real-time dashboard endpoint
- Fraud rate monitoring
- P95 latency metrics
- Streaming event aggregation
- Drift simulation
- Intentional schema corruption testing
- Operational observability

---

## Testing
- Concurrent load testing with Locust
- Synthetic fraud burst generation
- Edge-case transaction testing
- Invalid schema testing
- Data drift simulation
- Stress and resilience testing

---

# Tech Stack

| Category | Technology |
|---|---|
| ML Model | XGBoost |
| API Framework | FastAPI |
| Monitoring | Evidently AI |
| Event Streaming | Redis Streams |
| Load Testing | Locust |
| Containerization | Docker Compose |
| Language | Python 3.11 |
| Explainability | SHAP |

---

# System Design Goals

This project focuses on:
- production-oriented ML infrastructure
- low-latency fraud inference
- real-time observability
- distributed systems concepts
- operational ML engineering
- resilience under concurrency
- monitoring and drift detection

---

# Running The System

## Clone Repository

```bash
git clone <repo-url>
cd project
```

---

## Build Containers

```bash
docker compose up --build
```

---

# Service Endpoints

| Service | URL |
|---|---|
| API Gateway | http://127.0.0.1:8000 |
| Fraud Service | Internal Only |
| Monitoring Dashboard | http://127.0.0.1:8002/dashboard |
| Locust Dashboard | http://127.0.0.1:8089 |

---

# Example Prediction Request

```json
{
  "data": {
    "V1": -1.2,
    "V2": 0.8,
    "V3": -0.5,
    "V4": 2.1,
    "V5": -0.9,
    "V6": 0.3,
    "V7": -1.5,
    "V8": 0.1,
    "V9": -2.0,
    "V10": -1.7,
    "V11": 1.3,
    "V12": -0.8,
    "V13": 0.5,
    "V14": -2.2,
    "V15": 0.4,
    "V16": -1.1,
    "V17": -1.8,
    "V18": 0.7,
    "V19": 1.2,
    "V20": 0.3,
    "V21": 0.5,
    "V22": -0.4,
    "V23": 0.2,
    "V24": 0.1,
    "V25": -0.2,
    "V26": 0.3,
    "V27": 0.1,
    "V28": 0.05,
    "Amount": 89.25
  }
}
```

---

# Example Response

```json
{
  "status": "success",
  "prediction": {
    "fraud_probability": 0.9821,
    "decision": "BLOCK"
  }
}
```

---

# Locust Load Testing Dashboard

The system includes concurrent stress testing with synthetic fraud traffic generation.

![Locust Dashboard](locust%20graph.png)

---

# Drift & Chaos Testing

The platform intentionally supports:
- schema drift
- data drift
- adversarial fraud bursts
- malformed requests
- extreme feature values
- intentional misclassifications
- concurrency spikes

This enables realistic resilience validation for production-style ML systems.

---

# Future Improvements

- Kafka event streaming
- Kubernetes deployment
- Prometheus + Grafana
- Distributed tracing
- ONNX Runtime inference
- GPU inference serving
- Canary deployments
- Online model retraining
- Feature store integration

---
