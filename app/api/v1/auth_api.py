from fastapi import APIRouter, Depends, HTTPException
from app.core.jwt import create_access_token
from app.models.schemas import ResponseModel
from app.schemas.profile_schema import ProfileCreateRequest, SignInRequest, TokenVerificationRequest, UpdatePasswordRequest
from app.repositories.profile_repository import ProfileRepository
from app.services.email_service import send_verification_email
from pymongo import MongoClient
from app.core.config import settings

router = APIRouter()

# Initialize MongoDB client
client = MongoClient(settings.MONGO_URI)
db = client["VergoldWebDB"]

@router.post("/register", response_model=ResponseModel)
async def register(request: ProfileCreateRequest):
    profile_repo = ProfileRepository(db)

    if(profile_repo.email_exist(request.email)):
        raise HTTPException(status_code=400, detail="Email already registered.")
        

    token = profile_repo.save_profile_and_token(request.email)
    send_verification_email(request.email, token)

    data = {
        "Email Address": request.email,
        "Token" : token
        }
    return ResponseModel(status= "200", message="Verification email sent.", data= data)


@router.post("/verify", response_model=ResponseModel)
async def verify_token(request: TokenVerificationRequest):
    profile_repo = ProfileRepository(db)

    verified = profile_repo.verify_token(request.email, request.token)
    
    if verified:
        return ResponseModel(status= "200", message="Your email has been successfully verified.")
    else:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")
    
@router.patch("/update-password",response_model=ResponseModel)
async def update_password(request: UpdatePasswordRequest):
    profile_repo = ProfileRepository(db)
    
    # Check if the user exists
    if not profile_repo.email_exist(request.email):
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the password
    profile_repo.update_password(request.email, request.new_password)
    
    return ResponseModel(status= "200", message="Password updated successfully.")

@router.post("/signin", response_model=ResponseModel)
async def signin(request: SignInRequest):
    profile_repo = ProfileRepository(db)
    
    # Check if the email exists and verify the password
    if not profile_repo.email_exist(request.email):
        raise HTTPException(status_code=404, detail="User not found")
    
    if not profile_repo.verify_password(request.email, request.password):
        raise HTTPException(status_code=400, detail="Invalid User details")

    # Create JWT token
    access_token = create_access_token(data={"sub": request.email})

    get_profile = profile_repo.get_profile(request.email)

    get_profile_details = {"Email": get_profile["email"],
                           "UserId": get_profile["user_id"],
                           "IsVerified":get_profile["verified"]}

    data= {
        "access_token":access_token,
        "token_type":"bearer",
        "Profile Details": get_profile_details
    }
    return ResponseModel(status= "200", message="Login successful.", data= data)

    #return {"access_token": access_token, "token_type": "bearer"}


