from environs import Env
from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn


class Settings(BaseSettings):

    POSTGRES_USER: str = Field("postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("postgres", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("postgres", env="POSTGRES_DB")
    POSTGRES_HOST: str = Field("localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: int | str = Field("5432", env="POSTGRES_PORT")

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
