from datetime import date
from typing import Dict, List, Optional, Union
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, EmailStr

class ProfileCreateRequest(BaseModel):
    email: EmailStr

class ProfileResponse(BaseModel):
    email: EmailStr
    message: str

class TokenVerificationRequest(BaseModel):
    email: EmailStr
    token: str

class TokenVerificationResponse(BaseModel):
    email: EmailStr
    verified: bool
    message: str

class UpdatePasswordRequest(BaseModel):
    email: str
    new_password: str

class SignInRequest(BaseModel):
    email: str
    password: str

class Skill(BaseModel):
    skill_names: List[str]
    proficiency_levels: List[str]

class Certification(BaseModel):
   # title: str
    certificate_links: List[str]
    professional_certificate_files: List[UploadFile]


class Project(BaseModel):
    project_names: List[str]
    project_links: List[str]


class Education(BaseModel):
    levels: List[str]
    field_of_studies: List[str]
    institutions: List[str] 
    completion_dates: List[str]
    education_certificate_files: List[UploadFile]
    

class Experience(BaseModel):
    job_roles: List[str]
    durations: List[str]
    descriptions: List[str]


class JobAvailability(BaseModel):
    availability: Optional[str] 
    work_mode: Optional[str]
    cv_file: Optional[UploadFile]


class PersonalInformation(BaseModel):
    fullname: Optional[str] 
    email: Optional[str]
    profile_image: Optional[UploadFile]




# Dependency functions
def personal_information_form(
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    profile_image: UploadFile = File(None)
) -> PersonalInformation:
    personalInformation =  PersonalInformation(
        fullname= name,
        email= email,
        profile_image= profile_image
    )
    return personalInformation.dict()

def skill_form(
    skill_names: List[str] = Form(None),
    proficiency_levels: List[str] = Form(None)
) -> Skill:

    skill = Skill(skill_names = [skill_name for skill_name in skill_names], 
                 proficiency_levels = [proficiency_level for proficiency_level in proficiency_levels]
    )

    return skill.dict()

def certification_form(
    professional_certificate_files: List[UploadFile] = File(None),
    certificate_links: List[str] = Form(None)
) -> Certification:
    return Certification(professional_certificate_files = [file for file in professional_certificate_files], 
                         certificate_links = [certificate_link for certificate_link in certificate_links]
                         ).dict()

def project_form(
        project_names: List[str] = Form(None),
        project_links : List[str] = Form(None)
) -> Project:
    return Project(project_names = [project_name for project_name in project_names], 
                   project_links = [project_link for project_link in project_links]).dict()

def education_form(
        education_levels:List[str] = Form(None),
        education_field_of_studies:List[str] = Form(None),
        education_institutions :List[str] = Form(None),
        education_completion_dates: List[str] = Form(None),
        education_certificate_files: List[UploadFile] = File(None)
) -> Education:
    return Education(
        levels = [education_level for education_level in education_levels],
        field_of_studies = [education_field_of_studie for education_field_of_studie in education_field_of_studies],
        institutions = [education_institution for education_institution in education_institutions],
        completion_dates = [education_completion_date for education_completion_date in education_completion_dates],
        education_certificate_files =  [file for file in education_certificate_files]
    ).dict()

def experience_form(
        job_roles: List[str] = Form(None),
        durations: List[str] = Form(None),
        descriptions: List[str]= Form(None)
) -> Experience:
    return Experience(
        job_roles= [job_role for job_role in job_roles],
        durations= [duration for duration in durations],
        descriptions= [description for description in descriptions]
    ).dict()

def job_availability_form(
    availability: Optional[str] = Form(None),
    work_mode: Optional[str] = Form(None),
    cv_file: UploadFile = File(None)
) -> JobAvailability:
    return JobAvailability(
        availability= availability,
        work_mode= work_mode,
        cv_file= cv_file
    ).dict()

# class UpdateProfileRequest(BaseModel):
#     skills: Union[Dict, Skill]
#     certifications: Union[Dict, Certification]
#     projects: Union[Dict, Project]
#     educations: Union[Dict, Education]
#     experiences: Union[Dict, Experience]
#     job_availability: JobAvailability
#     personal_information: PersonalInformation

class UpdateProfileRequest(BaseModel):
    skills:  Skill
    certifications: Certification
    projects:  Project
    educations: Education
    experiences:  Experience
    job_availability: JobAvailability
    personal_information: PersonalInformation

# Function to parse form data and create ProfileForm
async def parse_profile_request_form(
    
    # Personal Information
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    profile_image: UploadFile = File(None),

    
    # Skills
    skill_names: List[str] = Form(None),
    skill_levels: List[str] = Form(None),

    # Certifications
    professional_certificate_files: List[UploadFile] = File(None),
    #certificate_titles: List[str] = Form(...),
    certificate_links: List[Optional[str]] = Form(None),

    # Projects
    project_names: List[str] = Form(None),
    project_links: List[Optional[str]] = Form(None),

    # Education
    educational_levels: List[str] = Form(None),
    educational_fields: List[str] = Form(None),
    educational_institutions: List[str] = Form(None),
    educational_date: List[date] = Form(None),
    education_certificate_files: List[UploadFile] = File(None),

    # Experience
    job_roles: List[str] = Form(None),
    job_durations: List[str] = Form(None),
    job_descriptions: List[str] = Form(None),

    # Job Availability
    availability: str = Form(None),
    work_mode: str = Form(None),
    cv_file: UploadFile = File(None)
):
    # Create lists of Pydantic models from the form data
    skills = [
        Skill(name=name, proficiency_level=level) 
        for name, level in zip(skill_names, skill_levels)
    ]
    certifications = [
        Certification(certificate_link=link, professional_certificate_files = professional_certificate_files) 
        for professional_certificate_files, link in zip(professional_certificate_files, certificate_links)
    ]
    projects = [
        Project(name=name, project_link=link) 
        for name, link in zip(project_names, project_links)
    ]
    education = [
        Education(level=level, field_of_study=field, institution=inst, completion_date=date, education_certificate_files= education_certificate_files) 
        for level, field, inst, date, education_certificate_files in zip(educational_levels, educational_fields, educational_institutions, educational_date, education_certificate_files)
    ]
    experiences = [
        Experience(job_role=role, duration=duration, description=description) 
        for role, duration, description in zip(job_roles, job_durations, job_descriptions)
    ]

    job_availability = JobAvailability(availability=availability, work_mode=work_mode, cv_file= cv_file)

    personal_information = PersonalInformation(name=name, email= email, profile_image= profile_image)

    
    profileRequest = UpdateProfileRequest(
        skills=skills,
        certifications=certifications,
        projects=projects,
        education=education,
        experiences=experiences,
        job_availability=job_availability,
        personal_information=personal_information
    )
    return profileRequest

