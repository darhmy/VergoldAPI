from fastapi import FastAPI
from app.api.v1 import auth_api, profile_api

app = FastAPI()

app.include_router(auth_api.router, prefix="/api/v1/auth", tags=["Authetication"])

app.include_router(profile_api.router, prefix="/api/v1/profile", tags=["Profile"])

