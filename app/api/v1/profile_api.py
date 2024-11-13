
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo import MongoClient
#from app.core.config import settings
import jwt
from app.models.schemas import ResponseModel
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile_schema import Certification, Education, Experience, JobAvailability, PersonalInformation, Project, Skill, UpdateProfileRequest, certification_form, education_form, experience_form, job_availability_form, personal_information_form, project_form, skill_form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from decouple import config

router = APIRouter()

mongoDBConnectionString = config("MONGO_URI")

jwtSecretKey = config("JWT_SECRET_KEY")
jwtAlgorithm = config("JWT_ALGORITHM")

# Initialize MongoDB client
client = MongoClient(mongoDBConnectionString)

db = client["VergoldWebAPIDB"]

# HTTP Bearer security scheme
bearer_scheme = HTTPBearer()

@router.patch("/update-profile", response_model=ResponseModel)
async def update_profile(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), personalInformation: PersonalInformation = Depends(personal_information_form), 
                                      skills: List[Skill] = Depends(skill_form),
                                      certifications: List[Certification] = Depends(certification_form),
                                      projects: List[Project] = Depends(project_form),
                                      educations: List[Education] = Depends(education_form),
                                      experiences: List[Experience] = Depends(experience_form),
                                      jobavailability: JobAvailability = Depends(job_availability_form)
                                      ):
    
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, jwtSecretKey, algorithms=[jwtAlgorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        else:
            profile_repo = ProfileRepository(db)

            # Check if the user exists
            if not profile_repo.get_profile_by_email(username):
                raise HTTPException(status_code = 404, detail="User not found")
            
            else:
                try:
                    profileRequest = UpdateProfileRequest(
                        skills = skills,
                        certifications = certifications,
                        projects= projects,
                        educations= educations,
                        experiences= experiences,
                        personal_information = personalInformation,
                        job_availability= jobavailability
                    )


                    await profile_repo.update_profile(profileRequest)
                    return ResponseModel(status= "200", message="Profile updated successfully.", data= None)
                except Exception as ex:
                    raise HTTPException(status_code=400, detail=f"Something went wrong.")
    
    except jwt.PyJWTError:
        raise credentials_exception