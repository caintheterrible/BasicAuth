"""Deploys module depending on debug settings from environment variable."""

import os
from dotenv import load_dotenv

load_dotenv()
django_env= os.getenv('DJANGO_ENV').lower()


if django_env== 'development':
    from app_config.settings.development import *
    print('Development environment deployed successfully!')
elif django_env== 'production':
    from app_config.settings.production import *
    print('Production environment deployed successfully!')
else:
    raise ValueError(
        f'Unexpected DJANGO_ENV variable!'
    )