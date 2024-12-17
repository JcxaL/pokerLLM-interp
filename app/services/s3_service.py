import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

class S3Service:
    def __init__(self):
        self.region_name = os.getenv('AWS_REGION', 'us-east-1')
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=self.region_name
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME')

    async def upload_file(self, file_data: bytes, file_name: str) -> str:
        try:
            # Upload the file
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=file_data,
                ContentType='image/jpeg'  # Adjust content type as needed
            )

            # Generate the standard public URL
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
            print(f"Generated URL: {url}")  # Add logging for debugging
            return url
        except ClientError as e:
            print(f"Error uploading to S3: {e}")
            raise