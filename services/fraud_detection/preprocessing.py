import numpy as np
from config import FEATURES

def preprocess(payload: dict):

    return np.array(
        [[payload[f] for f in FEATURES]],
        dtype=float
    )