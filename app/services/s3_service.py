import boto3
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from fastapi import File, UploadFile
#from app.core.config import settings
from decouple import config

awsRegion = config("AWS_REGION")
s3AccessKey = config("S3_ACCESS_KEY")
s3SecretKey = config("S3_SECRET_KEY")
s3BucketName = config("S3_BUCKET_NAME")

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=s3AccessKey,
            aws_secret_access_key=s3SecretKey,
            region_name=awsRegion
        )

    async def upload_file(self, file:UploadFile , file_type: str, email: str) -> str:
        #file_extension = file.filename.split(".")[-1]
        foldername = "VergoldWebFiles"
        unique_filename = f"{foldername}/{file_type}/{str(uuid.uuid4())}_{file.filename}"

        file_content = await file.read()


        #file_key = f"{foldername}/{file_type}/{email}_{uuid.uuid4()}"
       # .{file_extension}"

        try:
           self.s3_client.put_object(Bucket=s3BucketName, Key=unique_filename, Body=file_content)
            # self.s3_client.upload_fileobj(
            #     file,
            #     settings.S3_BUCKET_NAME,
            #     file_key
            #     #ExtraArgs={"ACL": "public-read"}
            # )
        except (NoCredentialsError, PartialCredentialsError) as e:
            raise Exception("AWS credentials not found or incomplete")
        except Exception as e:
            raise Exception(f"Failed to upload file to S3: {str(e)}")

        return f"https://{s3BucketName}.s3.{awsRegion}.amazonaws.com/{unique_filename}"
