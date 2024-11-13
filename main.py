from fastapi import FastAPI
from app.api.v1 import auth_api, profile_api

app = FastAPI()

app.include_router(auth_api.router, prefix="/api/v1/auth", tags=["Authetication"])

app.include_router(profile_api.router, prefix="/api/v1/profile", tags=["Profile"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Vergold Web API Documentation"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
