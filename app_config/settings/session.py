from typing import Dict, Union
from app_config.settings.cache import RedisCacheConfig

class RedisSessionConfig:
    """Redis session management configurations."""
    def __init__(self):
        self._redis_config= RedisCacheConfig()

    @property
    def session_config(self)-> Dict[str, Union[str, int, bool]]:
        return {
            'SESSION_ENGINE':'django.contrib.sessions.backends.cache',
            'SESSION_CACHE_ALIAS':'default',
            'SESSION_COOKIE_NAME':'sessionid',
            'SESSION_COOKIE_SECURE':True,
            'SESSION_COOKIE_HTTPONLY':True,
            'SESSION_COOKIE_AGE':120950,
            'SESSION_SAVE_EVERY_REQUEST':False,
            'SESSION_EXPIRE_AT_BROWSER_CLOSE':True,
        }


redis_session_config= RedisSessionConfig()