
import boto3
from botocore.exceptions import ClientError
from app.repositories.token_repository import TokenRepository
from app.core.config import settings

class EmailService:
    def __init__(self, token_repository: TokenRepository):
        self.token_repository = token_repository
        self.ses_client = boto3.client(
            "ses",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    def send_verification_email(self, email: str):
        token = self.token_repository.generate_token()
        self.token_repository.save_token(token, email)
        
        verification_link = f"{settings.BASE_URL}/verify-email/{token}"
        subject = "Verify your email address"
        body_html = f"""
        <html>
        <body>
          <h1>Verify your Email</h1>
          <p>Your verification code is: <strong>{token}</strong></p>
          <p>Or click on the link below to verify:</p>
          <a href='{verification_link}'>Verify Email</a>
        </body>
        </html>
        """

        try:
            response = self.ses_client.send_email(
                Destination={"ToAddresses": [email]},
                Message={
                    "Body": {"Html": {"Charset": "UTF-8", "Data": body_html}},
                    "Subject": {"Charset": "UTF-8", "Data": subject},
                },
                Source=settings.SENDER_EMAIL,
            )
            return {"message": "Verification email sent!"}
        except ClientError as e:
            raise Exception(f"Email failed to send: {str(e)}")

    def verify_email_token(self, token: str):
        email = self.token_repository.get_email_by_token(token)
        if not email:
            raise Exception("Invalid or expired token.")
        self.token_repository.delete_token(token)
        return f"Email {email} verified successfully!"
