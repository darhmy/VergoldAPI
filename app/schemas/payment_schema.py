from pydantic import BaseModel,EmailStr

class Payments(BaseModel):
  email: EmailStr
  amount: float
  phoneNumber: str
  fullName: str
  duration: int #No of days, weeks or months
  durationType: str #Daily, weekly or monthly
  paymentType: str #For CoWorking or Training
  paymentCategory: str #For coworking, it can be Solaria while for training it can be Backend

class PaystackWebhookPayload(BaseModel):
    event: str
    data: dict