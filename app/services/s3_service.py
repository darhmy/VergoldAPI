import boto3
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from fastapi import File, UploadFile
from app.core.config import settings

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.AWS_REGION
        )

    async def upload_file(self, file:UploadFile , file_type: str, email: str) -> str:
        #file_extension = file.filename.split(".")[-1]
        foldername = "VergoldWebFiles"
        unique_filename = f"{foldername}/{file_type}/{str(uuid.uuid4()).replace("-", "")}_{file.filename}"

        file_content = await file.read()


        #file_key = f"{foldername}/{file_type}/{email}_{uuid.uuid4()}"
       # .{file_extension}"

        try:
           self.s3_client.put_object(Bucket=settings.S3_BUCKET_NAME, Key=unique_filename, Body=file_content)
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

        return f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{unique_filename}"
