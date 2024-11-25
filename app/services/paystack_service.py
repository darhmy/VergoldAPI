import requests
from decouple import config

baseUrl = config("PaystackBaseUrl")
secretKey = config("PaystackSecretKey")

def accept_payments(email:str,amount:float, reference: str):
    url= f"{baseUrl}/transaction/initialize"
    headers = {
        "Authorization":f"Bearer {secretKey}",
    }
    data = {
        "email":email,
        "amount":amount * 100,
        "channels": ["card", "bank", "bank_transfer"],
        "reference": reference,
        "callback_url": f"https://vergoldapi.onrender.com/api/v1/payment/update-payment/{reference}"
        #"callback_url": f"http://127.0.0.1:8000/api/v1/payment/update-payment/{reference}"
    }
    
    try:
        response = requests.post(url,headers=headers,data=data)
        # response.raise_for_status()
        
        result = response.json()["data"]["authorization_url"]

        return result
    except requests.exceptions.HTTPError as e:
        return None
    
def verify_payment(reference:str):
    url =f"{baseUrl}/transaction/verify/{reference}"
    headers = {
        "Authorization":f"Bearer {secretKey}",
    }
    try:
        response = requests.get(url,headers=headers)
        result = response.json()["data"]["authorization_url"]

        return result
    except requests.exceptions.HTTPError as e:
        return None
