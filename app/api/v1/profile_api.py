
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pymongo import MongoClient
from app.core.config import settings
from app.models.schemas import ResponseModel
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile_schema import Certification, Education, Experience, JobAvailability, PersonalInformation, Project, Skill, UpdateProfileRequest, certification_form, education_form, experience_form, job_availability_form, personal_information_form, project_form, skill_form


router = APIRouter()

# Initialize MongoDB client
client = MongoClient(settings.MONGO_URI)
db = client["VergoldWebDB"]



@router.patch("/update-profile/{userId}", response_model=ResponseModel)
async def update_profile(userId: str, personalInformation: PersonalInformation = Depends(personal_information_form), 
                                      skills: List[Skill] = Depends(skill_form),
                                      certifications: List[Certification] = Depends(certification_form),
                                      projects: List[Project] = Depends(project_form),
                                      educations: List[Education] = Depends(education_form),
                                      experiences: List[Experience] = Depends(experience_form),
                                      jobavailability: JobAvailability = Depends(job_availability_form)
                                      ):
    profile_repo = ProfileRepository(db)

    # Check if the user exists
    if not profile_repo.get_profile_by_userId(userId):
        raise HTTPException(status_code = 404, detail="User not found")
    
    else:

        profileRequest = UpdateProfileRequest(
            skills = skills,
            certifications = certifications,
            projects= projects,
            educations= educations,
            experiences= experiences,
            personal_information = personalInformation,
            job_availability= jobavailability
        )


        profile_details = await profile_repo.update_profile(profileRequest)
        return ResponseModel(status= "200", message="Profile updated successfully.", data= None)
