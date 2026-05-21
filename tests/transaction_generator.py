import numpy as np
import random


# =========================================================
# FEATURE ORDER
# =========================================================

FEATURES = [f"V{i}" for i in range(1, 29)] + ["Amount"]


# =========================================================
# GOOD TRANSACTION
# Centered around mean
# =========================================================

def generate_good_transaction():

    x = np.random.normal(
        loc=0.0,
        scale=0.5,
        size=29
    )

    # Amount around normal range
    x[-1] = np.random.normal(loc=-0.25, scale=0.2)

    return x


# =========================================================
# FRAUD-LIKE TRANSACTION
# High variance + extreme PCA shifts
# =========================================================

def generate_fraud_transaction():

    x = np.random.normal(
        loc=0,
        scale=5,
        size=29
    )

    # Inject extreme suspicious behavior
    suspicious_indices = np.random.choice(
        range(28),
        size=10,
        replace=False
    )

    x[suspicious_indices] *= np.random.uniform(3, 8)

    # Larger transaction amount
    x[-1] = np.random.uniform(5, 100)

    return x


# =========================================================
# EDGE CASES
# Use dataset min/max style values
# =========================================================

MIN_VALUES = np.array([
    -56.4, -72.7, -48.3, -5.68, -113.7,
    -26.1, -43.5, -73.2, -13.4, -24.5,
    -10, -10, -10, -10, -10,
    -10, -10, -10, -10, -10,
    -34.8, -10.9, -44.8, -2.83, -10.2,
    -2.6, -22.5, -15.4, -0.35
])

MAX_VALUES = np.array([
    2.45, 22.0, 9.38, 16.8, 34.8,
    73.3, 120.5, 20.0, 15.5, 23.7,
    10, 10, 10, 10, 10,
    10, 10, 10, 10, 10,
    27.2, 10.5, 22.5, 4.58, 7.51,
    3.51, 31.6, 33.8, 102.3
])


def generate_edge_case():

    return np.where(
        np.random.rand(29) > 0.5,
        MAX_VALUES,
        MIN_VALUES
    )


# =========================================================
# DATA DRIFT
# Shift distributions
# =========================================================

def generate_drifted_transaction():

    x = np.random.normal(
        loc=3.0,
        scale=2.0,
        size=29
    )

    x[-1] = np.random.uniform(20, 80)

    return x


# =========================================================
# OUT-OF-VARIANCE
# Numerical stability tests
# =========================================================

def generate_out_of_variance_transaction():

    x = np.random.uniform(
        low=-1e6,
        high=1e6,
        size=29
    )

    return x


# =========================================================
# INVALID SCHEMA
# Intentionally malformed payload
# =========================================================

def generate_invalid_schema():

    return {
        "V1": "INVALID",
        "V2": [],
        "V3": {},
        "Amount": "ABCD"
    }


# =========================================================
# CONVERT NUMPY ARRAY → JSON PAYLOAD
# =========================================================

def to_payload(x):

    return {
        FEATURES[i]: float(x[i])
        for i in range(len(FEATURES))
    }


# =========================================================
# BULK GENERATORS
# =========================================================

def generate_batch(generator_fn, n=100):

    return np.array([
        generator_fn()
        for _ in range(n)
    ])


# =========================================================
# EXAMPLES
# =========================================================

good_tx = generate_good_transaction()

fraud_tx = generate_fraud_transaction()

edge_tx = generate_edge_case()

drift_tx = generate_drifted_transaction()

adversarial_tx = generate_out_of_variance_transaction()

invalid_schema = generate_invalid_schema()


# =========================================================
# JSON PAYLOADS
# =========================================================

good_payload = to_payload(good_tx)

fraud_payload = to_payload(fraud_tx)

edge_payload = to_payload(edge_tx)

drift_payload = to_payload(drift_tx)

adversarial_payload = to_payload(adversarial_tx)


# =========================================================
# BULK LOAD TEST DATA
# =========================================================

good_batch = generate_batch(
    generate_good_transaction,
    n=1000
)

fraud_batch = generate_batch(
    generate_fraud_transaction,
    n=100
)

drift_batch = generate_batch(
    generate_drifted_transaction,
    n=500
)