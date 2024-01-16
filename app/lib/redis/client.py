from redis import Redis


def get_redis_client():
    return Redis(host='redis', port=6379)


class RedisManager:
    def __init__(self):
        self.client = get_redis_client()

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value):
        return self.client.set(key, value)

    def delete(self, key):
        return self.client.delete(key)

    def keys(self, pattern):
        return self.client.keys(pattern)

    def flush(self):
        return self.client.flushall()

    def info(self):
        return self.client.info()

    def set_dict(self, key, value_dict: dict):
        return self.client.hmset(key, value_dict)

    def get_dict(self, key):
        return self.client.hgetall(key)

    def __repr__(self):
        return f'<RedisManager: {self.client}>'
