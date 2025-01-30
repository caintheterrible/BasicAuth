"""Base configuration module for Django application."""

import os
from pathlib import Path
from typing import List, Dict, Any
from app_config.settings.cache import redis_cache_config
from app_config.settings.session import redis_session_config
from app_config.settings.database import postgresql_config
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    """Core configurations handling Django."""
    def __init__(self):
        self._secret_key= os.getenv('DJANGO_SECRET_KEY')
        self.base_dir= Path(__file__).resolve().parent.parent.parent
        self._db_config= postgresql_config().django_db_config
        self._validate_environment()
        self._caching= redis_cache_config.cache_settings
        self._session= redis_session_config.session_config

    @staticmethod
    def _validate_environment()-> None:
        """Validates required environment variables if existing."""
        required_fields=[
            'DJANGO_SECRET_KEY',
            'DB_NAME',
            'DB_USER',
            'DB_PSWD',
            'DB_HOST',
            'DB_PORT',
        ]
        missing_variable= [variable for variable in required_fields if not os.getenv(variable)]
        if missing_variable:
            raise ValueError(f'Missing required environment variables: {', '.join(missing_variable)}')

    @property
    def secret_key(self)-> str:
        """Secure secret key getter with validation."""
        if not self._secret_key:
            raise ValueError(f'SECRET_KEY environment variable expected but undefined.')
        return self._secret_key

    @property
    def installed_apps(self)-> List[str]:
        """Installed applications list to separate from third party and project defined applications."""
        THIRD_PARTY_APPS=[
            'corsheaders',
            'django_redis',
            'celery',
        ]
        PROJECT_APPS=[]
        return THIRD_PARTY_APPS+ PROJECT_APPS

    @property
    def cache(self)-> Dict[str, Dict[str, Any]]:
        """Cache configurations."""
        return self._caching

    @property
    def session(self)-> Dict[str, Dict[str, Any]]:
        """Session management configurations."""
        return self._session

    @property
    def database(self)-> Dict[str, Dict[str, Any]]:
        """Database configurations."""
        return self._db_config

    @property
    def middleware(self)-> List[str]:
        """
        List of middleware employed in application.
        CAUTION: Order of list arrangement is crucial for expected application functioning!
        """
        middleware_default= [
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
        ]
        middleware_defined= [] # custom middleware here

        return middleware_default + middleware_defined


@lru_cache()
def base_config()-> BaseConfig:
    """Cached configuration instance."""
    return BaseConfig()


config= base_config()

SECRET_KEY= config.secret_key
BASE_DIR= config.base_dir
# DATABASES= config.database (now configured in development.py application run point to avoid ImproperlyConfigured errors during migrate.)
CACHES= config.cache
MIDDLEWARE= config.middleware
INSTALLED_APPS= config.installed_apps

# Session Management
SESSION_ENGINE= config.session['SESSION_ENGINE']
SESSION_CACHE_ALIAS= config.session['SESSION_CACHE_ALIAS']
SESSION_COOKIE_NAME= config.session['SESSION_COOKIE_NAME']
SESSION_COOKIE_SECURE= config.session['SESSION_COOKIE_SECURE']
SESSION_COOKIE_HTTPONLY= config.session['SESSION_COOKIE_HTTPONLY']
SESSION_COOKIE_AGE= config.session['SESSION_COOKIE_AGE']
SESSION_SAVE_EVERY_REQUEST= config.session['SESSION_SAVE_EVERY_REQUEST']

# Deployment support
ASGI_APPLICATION= 'app_config.asgi.application'
WSGI_APPLICATION= 'app_config.wsgi.application'

# Security
CSRF_TRUSTED_ORIGINS= []

# Other
LANGUAGE_CODE= 'en-us'
TIME_ZONE= 'UTC'
USE_L10N= True
USE_I10N= True
USE_TZ= True