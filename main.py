from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth_api, profile_api, payment_api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth_api.router, prefix="/api/v1/auth", tags=["Authetication"])

app.include_router(profile_api.router, prefix="/api/v1/profile", tags=["Profile"])

app.include_router(payment_api.router, prefix="/api/v1/payment", tags=["Payment"])

@app.post("/webhook")
async def paystack_webhook(request: Request):
    result = await request.json()
    print(result)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Vergold Web API Documentation"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
