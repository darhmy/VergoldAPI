
from app.crud.payment_crud import PaymentCRUD
from app.schemas.payment_schema import Payments


class PaymentRepository:
    def __init__(self, db):
        self.payment = PaymentCRUD(db)

    def save_payment(self, paymentDetails: Payments):
        return self.payment.save_payment(paymentDetails)

    def update_payment(self, reference):
        return self.payment.update_payment(reference)