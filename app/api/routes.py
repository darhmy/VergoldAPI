
# from fastapi import APIRouter, HTTPException
# from app.models.schemas import CreateAccountRequest
# #from app.repositories.create_account_repository import TokenRepository
# from app.services.email_service import EmailService

# router = APIRouter()

# # Initialize repository and service
# #token_repository = TokenRepository()
# email_service = EmailService(token_repository)

# @router.post("/create-account/")
# def create_account(request: CreateAccountRequest):
#     try:
#         response = email_service.send_verification_email(request.email)
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/verify-email/{token}")
# def verify_email(token: str):
#     try:
#         message = email_service.verify_email_token(token)
#         return {"message": message}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
