
import attr
from redis import Redis
from pyramid.decorator import reify


@attr.s
class RedisStore(dict):

    url = attr.ib(default='redis://127.0.0.1:6379')
    name = attr.ib(default='redis_store')

    @reify
    def client(self):
        return Redis.from_url(self.url)
            
    def load(self):
        self.clear()
        self.update(self.client.hgetall(self.name))

    def _destroy(self):
        self.client.delete(self.name)

    def __missing__(self, key):

        val = self.client.hget(self.name, key)
        if val is None:
            raise KeyError(key)

        self[key] = val
        return self[key]
        
    def __setitem__(self, key, value):
        self.client.hset(self.name, key, value)
        super(RedisStore, self).__setitem__(key, value)

    def __delitem__(self, key):
        self.client.hdel(self.name, key)
        super(RedisStore, self).__delitem__(key)
        
