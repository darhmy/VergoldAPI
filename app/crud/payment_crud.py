

from datetime import datetime
import random
import uuid
from app.schemas.payment_schema import Payments
from app.services.paystack_service import accept_payments


class PaymentCRUD:
    def __init__(self, db):
        self.payment_collection = db["payments"]

    def generate_reference(self) -> str:
        return "Vergold-" + str(uuid.uuid4()).replace('-', '')[:5]

    def save_payment(self, paymentDetails: Payments):

        dt = datetime.now()

        # Random seed
        factor = random.Random(1)

        # List of characters
        chars = ["AB", "AC", "AD", "BC", "BD", "CD", "DC", "EF", "EG", "EH", "FG", "FH", "GH"]

        # Generate the transaction string
        trns = (f"{str(dt.year)[2:]}{dt.timetuple().tm_yday:03d}{dt.hour:02d}{dt.minute:02d}"
                f"{dt.second:02d}{chars[factor.randint(0, 11)]}")

        # Generate the transaction reference
        trans_reference = f"Vergold-{trns}"

        #refrence = "Vergold-" + str(uuid.uuid4()).replace('-', '')[:5]

        payment = {
            "Fullname": paymentDetails.fullName,
            "Email": paymentDetails.email,
            "PhoneNumber": paymentDetails.phoneNumber,
            "Status": "Pending",
            "TrasactionRefernce" : trans_reference,
            "Amount": paymentDetails.amount,
            "PaymentType": paymentDetails.paymentType,
            "PaymentCategory": paymentDetails.paymentCategory,
            "DateCreated": datetime.now(),
        }

        self.payment_collection.insert_one(payment)

        payment_url = accept_payments(email = paymentDetails.email, amount = paymentDetails.amount,
                                       reference = trans_reference)

        return payment_url
    
    def update_payment(self,reference):
        payment = self.payment_collection.find_one({"TrasactionRefernce":reference})

        if(payment is not None):
            self.payment_collection.update_one(
                {"TrasactionRefernce": reference},
            {"$set": {"Status": "Successful", "DateUpdated": datetime.now()}})
            return True
        else:
            return False
            