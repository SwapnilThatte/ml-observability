# Real-Time ML based Financial Fraud Detection Pipeline & ML Observability

This repository contains an end-to-end local machine learning inference pipeline designed for real-time transaction fraud detection. It features an API Gateway microservice, a dedicated Fraud Detection Service utilizing an XGBoost model, and a pre-configured local load-testing suite to simulate and monitor heavy traffic in a completely containerized, isolated environment.

## 📌 Architecture Overview

The system is split into independent local microservices running inside a secure, closed loopback Docker network:

* **API Gateway (`services/api/`):** Acts as the primary entry point for inbound transaction payloads, exposing a fast, lightweight REST interface.
* **Fraud Detection Service (`services/fraud_detection/`):** Houses the intelligence engine. It loads model weights, preprocesses transaction vectors, and runs data through an XGBoost model to evaluate fraud risk.
* **Load Test Runner (`tests/`):** Programmatically manages user simulation using Locust, generating realistic and anomalous data profiles.

---

## 🔒 Security & Isolation Features

This architecture is engineered for **strict local machine isolation (air-gapped execution)**:

* **Zero Internet Telemetry:** All inter-service communications utilize Docker’s internal bridge service discovery network. No outbound internet connections are made.
* **Network Isolation:** The Locust Web Dashboard and API Gateway are bound strictly to your host machine's loopback interface (`127.0.0.1`). Other nodes on your local Wi-Fi or local area network cannot access your endpoints, ensuring complete data privacy during active test simulations.
* **Minimalist Footprint:** All default `EXPOSE` directives have been omitted from the Dockerfiles to ensure no passive port mapping leaks to the host operating system.

---

## 🛠️ Actual Project Structure

```text
├── services/
│   ├── api/
│   │   ├── main.py                # FastAPI Gateway
│   │   ├── client.py              # Internal routing logic to Fraud Service
│   │   ├── schemas.py             # Shared Pydantic data validation schemas
│   │   ├── URL_DIR.py             # Service location registry
│   │   ├── requirements.txt       # Gateway package dependencies
│   │   └── Dockerfile             # Container configuration for API Gateway
│   └── fraud_detection/
│       ├── main.py                # Fraud Service App Entrypoint
│       ├── config.py              # Operational thresholds (Block/Review limits)
│       ├── model.py               # XGBoost model loader wrapper
│       ├── preprocessing.py       # Data scaler/preprocessor
│       ├── schemas.py             # Model-specific Pydantic data schemas
│       ├── xgboost_fraud_model.json # Serialized XGBoost model weights
│       ├── requirements.txt       # ML service dependencies (xgboost, etc.)
│       └── Dockerfile             # Container configuration for Inference Engine
└── tests/
    ├── loadtest.py                # Locust programmatic load test script
    ├── transaction_generator.py   # Mock payload helper utilities
    ├── unit_tests.py              # Local testing verification scripts
    ├── requirements.txt           # Tester package dependencies
    └── Dockerfile                 # Container configuration for Load Suite