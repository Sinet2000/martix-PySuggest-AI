from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Recommendation Engine"
    kafka_broker_url: str = "localhost:9092"

    class Config:
        env_file = ".env"

settings = Settings()
