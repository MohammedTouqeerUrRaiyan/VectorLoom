from cachetools import TTLCache


class CacheService:
    """
    In-memory cache for retrieval results.
    """

    _cache = TTLCache(
        maxsize=1000,
        ttl=300
    )

    @classmethod
    def get(cls, key):

        return cls._cache.get(key)

    @classmethod
    def set(cls, key, value):

        cls._cache[key] = value

    @classmethod
    def clear(cls):

        cls._cache.clear()