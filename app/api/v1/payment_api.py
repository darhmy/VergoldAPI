from fastapi import APIRouter,HTTPException, Request,status

from app.models.schemas import ResponseModel
from app.schemas.payment_schema import Payments, PaystackWebhookPayload
from app.repositories.payment_repository import PaymentRepository

from pymongo import MongoClient
from decouple import config

router = APIRouter()

mongoDBConnectionString = config("MONGO_URI")
# Initialize MongoDB client
client = MongoClient(mongoDBConnectionString)
db = client["VergoldWebAPIDB"]

# @router.post("discount/{code}", response_model= ResponseModel)
# async def discount(code:str):


@router.post("/initialize-payment/", response_model=ResponseModel)
async def initialize_payment(payment_details:Payments):
  

  paymentRepo = PaymentRepository(db)

  payment = paymentRepo.save_payment(payment_details)

  #print(f"Payment type is {type(payment)}")
  
  if payment is None:
    return HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Invalid request")
  
  return ResponseModel(status= "200", message="Successful.", data= payment)
  #return {"payment_url":payment}

@router.get("/update-payment/{reference}", response_model=ResponseModel)
async def update_payment(reference:str):
  
  paymentRepo = PaymentRepository(db)

  updatePayment = paymentRepo.update_payment(reference)

  if(updatePayment is True):
    return ResponseModel(status= "200", message="Successful.", data= None)
  else:
    return HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Invalid request")

@router.post("/webhook/paystack")
async def paystack_webhook(request: Request):
    result = await request.json()
    print(result)
    # if payload.event == "charge.success":
    #     payment_data = payload.data
    #     # Do something with payment data
    #     # Example: Save payment data to database, send email to customer, update order status, etc.
    #     return {"message":"Payment successful"} # redirect to a payment succesful page
    # return {"message":"Payment failed"} # can also redirect users to a page to try again or contact support

