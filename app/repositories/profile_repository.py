import random
from app.crud.profile_crud import ProfileCRUD
from app.schemas.profile_schema import UpdateProfileRequest

class ProfileRepository:
    def __init__(self, db):
        self.profile = ProfileCRUD(db)
    
    def generate_token(self):
        return str(random.randint(100000, 999999))
    
    def get_profile(self, email:str):
       return  self.profile.get_profile(email)
    
    def get_profile_by_userId(self, userId:str):
       return  self.profile.get_profile_by_userId(userId)

    
    def email_exist(self, email: str) -> bool:
         # Check if the email already exists
        if self.profile.email_exists(email):
            return True
            #return {"error": "Email already registered."}
        else:
            return False
        
    def save_profile_and_token(self, email: str):
        
        token = self.generate_token()
        self.profile.create_profile(email)         # Save email in "profiles" collection
        self.profile.save_token(email, token)      # Save token in "tokens" collection
        return token
    
    def verify_token(self, email: str, token: str):
        return self.profile.verify_token(email, token)
    
    def update_password(self, email: str, password: str):
        return self.profile.update_password(email,password)
    
    def verify_password(self, email: str, password: str):
        return self.profile.verify_password(email, password)
    
    async def update_profile(self, profileRequest: UpdateProfileRequest):
        return await self.profile.update_profile(profileRequest)
