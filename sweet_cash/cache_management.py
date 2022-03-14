
from app import redis
import pickle


class RedisCache(object):

    @staticmethod
    def setex(key: str, time, obj):
        value = pickle.dumps(obj)
        redis.setex(key, time, value)

    @staticmethod
    def get(key: str):
        value = redis.get(key)

        if value is None:
            return None

        return pickle.loads(value)

    @staticmethod
    def delete(key: str):
        redis.delete(key)
