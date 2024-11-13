import jwt
from datetime import datetime, timedelta
from decouple import config
#from app.core.config import settings

jwtSecretKey = config("JWT_SECRET_KEY")
jwtAlgorithm = config("JWT_ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Set in config

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,key= jwtSecretKey, algorithm=jwtAlgorithm)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, jwtSecretKey, algorithms=[jwtAlgorithm])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
