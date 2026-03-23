from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://tripuser:trippass@db:5432/tripdb"

    class Config:
        env_file = ".env"

settings = Settings()
