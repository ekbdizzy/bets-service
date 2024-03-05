import aioredis
from environs import Env
from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn


class Settings(BaseSettings):

    POSTGRES_USER: str = Field("postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("postgres", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("postgres", env="POSTGRES_DB")
    POSTGRES_HOST: str = Field("localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: int | str = Field("5432", env="POSTGRES_PORT")
    REDIS_HOST: str = Field("redis://redis:6379", env="REDIS_HOST")

    class Config:
        env = Env().read_env()

    def get_postgres_uri(self) -> PostgresDsn:
        uri = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            name=self.POSTGRES_DB,
        )
        return uri


settings = Settings()
redis = aioredis.from_url(settings.REDIS_HOST, encoding="utf-8", decode_responses=True)
