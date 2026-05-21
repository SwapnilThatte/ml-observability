import redis
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("redis-client")


def get_redis_connection():

    try:

        client = redis.Redis(
            host="redis",
            port=6379,
            decode_responses=True
        )

        client.ping()

        logger.info(
            "Connected to Redis"
        )

        return client

    except Exception as e:

        logger.exception(
            "Redis connection failed"
        )

        raise e


redis_client = get_redis_connection()