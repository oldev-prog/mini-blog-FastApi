from pydantic_settings import BaseSettings, SettingsConfigDict
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = '5432'
    DB_USER: str = 'postgres'
    DB_PASS: str = '12345'
    DB_NAME: str = 'mini_blog'

    @property
    def DATABASE_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def DATABASE_URL_psycopg(self):
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file=os.path.join(ROOT_DIR, '.env'))

settings = Settings()

