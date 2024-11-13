import uuid
#import bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from argon2 import PasswordHasher, exceptions

from app.models.dto import serializeDict
from app.schemas.profile_schema import UpdateProfileRequest
from app.services import s3_service

class ProfileCRUD:
    def __init__(self, db):
        self.profiles_collection = db["profiles"]
        self.tokens_collection = db["tokens"]
        self.s3Service = s3_service.S3Service()

    def create_profile(self, email: str):
        profile = {
            "email": email,
            "user_id": str(uuid.uuid4()).replace("-", "")[:16],
            "created_at": datetime.now(),
            "verified": False
        }
        self.profiles_collection.insert_one(profile)

    def get_profile(self, email: str):
         profile = self.profiles_collection.find_one({"email": email}) 
         if profile is not None:
             return serializeDict(profile)
         else:
             return None
         
    def get_profile_by_email(self, userId: str):
         profile = self.profiles_collection.find_one({"email": userId}) 
         if profile is not None:
             return serializeDict(profile)
         else:
             return None

    def save_token(self, email: str, token: str):
        token_entry = {
            "email": email,
            "token": token,
            "created_at": datetime.now(),
            "used": False
        }
        self.tokens_collection.insert_one(token_entry)

    def verify_token(self, email: str, token: str):
        # Check if the token exists and is not used
        token_data = self.tokens_collection.find_one({
            "email": email,
            "token": token,
            "used": False
            #"created_at": {"$gte": datetime.utcnow() - timedelta(minutes=10)}  # Token valid for 10 minutes
        })
        
        if token_data:
            # Mark token as used
            self.tokens_collection.update_one(
                {"_id": token_data["_id"]},
                {"$set": {"used": True}}
            )
            # Update profile to verified
            self.profiles_collection.update_one(
                {"email": email},
                {"$set": {"verified": True}}
            )
            return True
        return False
    
    def email_exists(self, email: str) -> bool:
        # Check if the email already exists in the profiles collection
        return self.profiles_collection.find_one({"email": email}) is not None
    
    # def hash_password(self, password: str) -> str:
    #     salt = bcrypt.gensalt()
    #     return bcrypt.hashpw(password.encode("utf-8"), salt)

    def update_password(self, email: str, new_password: str):
        #hashed_password = self.hash_password(new_password)

        ph = PasswordHasher()
        
        hashed_password = ph.hash(password= new_password)
        self.profiles_collection.update_one(
            {"email": email},
            {"$set": {"password": hashed_password, "updated_at": datetime.now()}}
        )

    def verify_password(self, email: str, password: str) -> bool:
        # Retrieve the user's stored password hash
        try:
            ph = PasswordHasher()
            user = self.profiles_collection.find_one({"email": email})
            if(ph.verify(hash= user["password"], password= password)):
                return True
            else:
                return False
            # if user and "password" in user:
            #     return bcrypt.checkpw(password.encode("utf-8"), user["password"])
            # return False
        except exceptions.VerifyMismatchError:
            return False
        
    async def update_profile(self, profileRequest: UpdateProfileRequest):
        user = self.profiles_collection.find_one({"email": profileRequest.personal_information.email})
        
        if user is not None:

            cv_upload_link = await self.s3Service.upload_file(profileRequest.job_availability.cv_file, "CV", profileRequest.personal_information.email)

            profile_image_link = await self.s3Service.upload_file(profileRequest.personal_information.profile_image, "ProfileImages", profileRequest.personal_information.email)

            if(len(profileRequest.certifications.professional_certificate_files) > 0):
                for certificate_file in profileRequest.certifications.professional_certificate_files:
                    profession_certificate_file_link = await self.s3Service.upload_file(certificate_file, "ProfessionalCertificate", profileRequest.personal_information.email)


            if(len(profileRequest.educations.education_certificate_files) > 0):
                for education_certificate_file in profileRequest.educations.education_certificate_files:

                    education_certificate_file_link = await self.s3Service.upload_file(education_certificate_file, "EducationalCertificate", profileRequest.personal_information.email)

            profile_dict = profileRequest.dict()

            profile_dict.update(
                {
                    "CV_Link": cv_upload_link,
                    "Profile_Image_Link": profile_image_link,
                    "Profession_Certificate_File_Link": profession_certificate_file_link,
                    "Education_Certificate_File_Link": education_certificate_file_link
                })
            
            profile_dict['certifications'].pop('professional_certificate_files', None)
            profile_dict['educations'].pop('education_certificate_files', None)
            profile_dict['job_availability'].pop('cv_file', None)
            profile_dict['personal_information'].pop('profile_image', None)
            
            
            self.profiles_collection.update_one({"email": profileRequest.personal_information.email}, {"$set": profile_dict})

            get_profile = self.profiles_collection.find_one({"email": profileRequest.personal_information.email})
            return serializeDict(get_profile)
        else:
            return None



