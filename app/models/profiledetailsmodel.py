from pydantic import BaseModel, EmailStr

class ProfileDetails(BaseModel):
    email: EmailStr