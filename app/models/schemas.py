from pydantic import BaseModel, EmailStr
from typing import Any, Optional, List

# Standardized response model
class ResponseModel(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None

# Standardized response list model
class ResponseListModel(BaseModel):
    status: str
    message: str
    data: Optional[List[Any]] = None

class CreateAccountRequest(BaseModel):
    email: EmailStr

