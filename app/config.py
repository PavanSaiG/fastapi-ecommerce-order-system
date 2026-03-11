from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Event Driven E-Commerce Order Processing System"
    DATABASE_URL: str = "sqlite:///./ecommerce.db"
    SECRET_KEY: str = "your-secret-key-for-jwt-super-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
