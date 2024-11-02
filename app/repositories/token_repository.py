# app/repositories/token_repository.py
import random
from pymongo import MongoClient
from app.core.config import settings

class TokenRepository:
    def __init__(self):
        # Initialize MongoDB client and select the database and collection
        self.client = MongoClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]
        self.collection = self.db["verification_tokens"]

    def generate_token(self):
        """Generate a random 6-digit token."""
        return str(random.randint(100000, 999999))

    def save_token(self, token: str, email: str):
        """Save a token-email pair to MongoDB, with upsert to avoid duplicates."""
        self.collection.insert_one(
            {"email": email},
            {"$set": {"token": token}}
        )

    def get_email_by_token(self, token: str):
        """Retrieve an email by token."""
        result = self.collection.find_one({"token": token})
        return result["email"] if result else None

    def delete_token(self, token: str):
        """Delete a token after verification."""
        self.collection.delete_one({"token": token})
