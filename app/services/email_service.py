from aiosmtplib import send
import boto3
from fastapi import BackgroundTasks
from app.core.config import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


async def send_email(subject: str, recipient: str, html_content:str, clientRefrence : str, secretRefrence: str,
                     configReference: str, port: int):
    message = MIMEMultipart()
    message["From"] = clientRefrence
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(html_content, "html"))

    await send(
        message,
        hostname= configReference,
        port=port,
        username=clientRefrence,
        password=secretRefrence,
       # start_tls=True,
    )


def send_verification_email(email: str, token: str):

    client = boto3.client(
        "ses",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.SES_ACCESS_KEY,
        aws_secret_access_key=settings.SES_SECRET_KEY,
    )
    
    subject = "Your Verification Code"
    body = f"Your verification code is: {token}"
    
    response = client.send_email(
        Source=settings.FROM_EMAIL,
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}},
        }
    )
    return response
