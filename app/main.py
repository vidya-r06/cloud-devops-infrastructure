import os

import boto3
from fastapi import FastAPI
app = FastAPI(title="Cloud DevOps Infrastructure API")

LOCALSTACK_HOST = os.getenv("LOCALSTACK_HOST", "localhost")

s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{LOCALSTACK_HOST}:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
)

BUCKET_NAME = "devops-project-terraform"


@app.get("/")
def root():
    return {
        "message": "Cloud DevOps Infrastructure API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/storage")
def storage():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    objects = []

    for item in response.get("Contents", []):
        objects.append(item["Key"])

    return {
        "bucket": BUCKET_NAME,
        "objects": objects
    }


@app.post("/storage/{filename}")
def upload_file(filename: str):
    content = f"File created by Cloud DevOps API: {filename}"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=content.encode("utf-8"),
    )

    return {
        "message": "File uploaded successfully",
        "bucket": BUCKET_NAME,
        "filename": filename,
    }