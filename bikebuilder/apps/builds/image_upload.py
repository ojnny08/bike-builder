import os
import uuid
from urllib.parse import urlparse
import boto3
from django.conf import settings


def _client():
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )


def upload_to_s3(file, build_id):
    ext = os.path.splitext(file.name)[1]
    key = f"user-upload/{build_id}-{uuid.uuid4().hex}{ext}"
    _client().put_object(
        Body=file.read(),
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=key,
        ContentType=file.content_type,
    )
    return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{key}"


def delete_from_s3(url):
    if not url:
        return
    key = urlparse(url).path.lstrip('/')
    _client().delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
