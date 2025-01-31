import os
from functools import lru_cache
from typing import Dict, Any
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from applications.shared.base import BaseModel

load_dotenv()
Base= declarative_base(cls=BaseModel)

class DatabaseConfig:
    """Database configurations."""
    def __init__(self):
        self.pg_user= os.getenv('DB_USER')
        self.pg_pswd= os.getenv('DB_PSWD')
        self.pg_host= os.getenv('DB_HOST')
        self.pg_port= os.getenv('DB_PORT')
        self.pg_db= os.getenv('DB_NAME')

    @property
    def postgresql_url(self)-> str:
        """Postgresql database URI."""
        return (f'postgresql://{self.pg_user}:{self.pg_pswd}@'
                f'{self.pg_host}:{self.pg_port}/{self.pg_db}')

    @property
    def django_db_config(self)-> Dict[str, Dict[str, Any]]:
        """Default Django database configuration."""
        return {
            'default':{
                'ENGINE':'django.db.backends.postgresql',
                'NAME':self.pg_db,
                'USER':self.pg_user,
                'PASSWORD':self.pg_pswd,
                'HOST':self.pg_host,
                'PORT':self.pg_port,
                'CONN_MAX_AGE':60,
                'OPTIONS':{
                    'connect_timeout':10,
                    'sslmode':'require',
                }
            }
        }


@lru_cache()
def postgresql_config()-> DatabaseConfig:
    """Returns a cached instance of the database configuration."""
    return DatabaseConfig()

def init_postgresql()-> sessionmaker:
    config= postgresql_config()
    engine= create_engine(config.postgresql_url)

    from applications.auth.auth_models import ClientUser
    Base.metadata.create_all(bind=engine)
    return sessionmaker(
        autoflush=False,
        autocommit=False,
        bind=engine
    )

SessionLocal= init_postgresql()