from aiosmtplib import send
import boto3
from fastapi import BackgroundTasks
#from app.core.config import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config

awsRegion = config("AWS_REGION")

sesAccesskey = config("SES_ACCESS_KEY")
sesSecretKey = config("SES_SECRET_KEY")

fromMail = config("FROM_EMAIL")



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

    try:

        client = boto3.client(
            "ses",
            region_name=awsRegion,
            aws_access_key_id=sesAccesskey,
            aws_secret_access_key=sesSecretKey,
        )
        
        subject = "Your Verification Code"
        body = f"Your verification code is: {token}"
        
        response = client.send_email(
            Source=fromMail,
            Destination={"ToAddresses": [email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}},
            }
        )
        return response
    except Exception as e:
        raise Exception(f"Failed to send mail : {str(e)}")
