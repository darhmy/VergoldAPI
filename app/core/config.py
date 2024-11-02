import os
from pydantic_settings import BaseSettings

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI")
    AWS_REGION: str = os.getenv("AWS_REGION")
    SES_ACCESS_KEY: str = os.getenv("SES_ACCESS_KEY")
    SES_SECRET_KEY: str = os.getenv("SES_SECRET_KEY")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL")

    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME")

    # JWT settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")  # Use a secure, random key in production
    JWT_EXPIRATION_MINUTES = 60  # 1 hour or as desired

settings = Settings()

