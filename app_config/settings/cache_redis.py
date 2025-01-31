import os
from typing import Dict, Any
from urllib.parse import quote
from redis import ConnectionPool, Redis
from dotenv import load_dotenv

load_dotenv()


class RedisCacheConfig:
    """Caching configurations with Redis."""

    def __init__(self):
        self._redis_host = os.getenv('REDIS_HOST', 'localhost')
        self._redis_port = int(os.getenv('REDIS_PORT', 6379))
        self._redis_db = int(os.getenv('REDIS_DB', 0))
        self._redis_pswd = os.getenv('REDIS_PSWD')

        if not self._redis_host:
            raise ValueError("REDIS_HOST environment variable is not set.")

    @property
    def redis_url(self) -> str:
        """Returns the Redis connection URL."""
        if self._redis_pswd:
            encoded_password = quote(self._redis_pswd)
            return f'redis://:{encoded_password}@{self._redis_host}:{self._redis_port}/{self._redis_db}'
        return f'redis://{self._redis_host}:{self._redis_port}/{self._redis_db}'

    @property
    def cache_settings(self) -> Dict[str, Dict[str, Any]]:
        """Returns Django Redis cache settings."""
        return {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': self.redis_url,
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.cache.DefaultClient',
                    'CONNECTION_POOL_KWARGS': {
                        'max_connections': 100,
                        'retry_on_timeout': True,
                    },
                },
            }
        }

    @property
    def cache_ttl(self) -> int:
        """Returns the default cache TTL (time-to-live) in seconds."""
        return int(os.getenv('CACHE_TTL', 300))

    @property
    def redis_connect(self) -> ConnectionPool:
        """Returns a Redis connection pool."""
        return ConnectionPool.from_url(
            self.redis_url,
            max_connections=100,
            socket_timeout=5,
            socket_keepalive=True,
            retry_on_timeout=True,
        )

    def test_redis_connection(self):
        """Tests the Redis connection."""
        try:
            r = Redis(connection_pool=self.redis_connect)
            r.ping()
            print("Redis connection successful!")
        except Exception as e:
            print(f"Redis connection failed: {e}")


# Singleton instance
redis_cache_config = RedisCacheConfig()

print(redis_cache_config.test_redis_connection())