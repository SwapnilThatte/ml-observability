from collections import deque
from redis_client import redis_client
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("dashboard")


# =========================================================
# IN-MEMORY ROLLING BUFFER
# =========================================================

BUFFER = deque(maxlen=5000)

LAST_ID = "0-0"


# =========================================================
# FETCH STREAM EVENTS
# =========================================================

def fetch_stream_events():

    global LAST_ID

    try:

        events = redis_client.xread(
            {"fraud_events": LAST_ID},
            count=100,
            block=1000
        )

        if not events:
            return

        for _, messages in events:

            for message_id, data in messages:

                LAST_ID = message_id

                BUFFER.append(data)

        logger.info(
            f"Fetched {len(BUFFER)} events"
        )

    except Exception as e:

        logger.exception(
            "Failed to fetch stream events"
        )