class IdempotencyService:

    def __init__(self):
        self.cache = {}

    def check(self, key):
        return self.cache.get(key)

    def store(self, key, response):
        self.cache[key] = response