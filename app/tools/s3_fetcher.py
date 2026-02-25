import boto3
from typing import Optional
from app.core.config import settings

def get_s3_client():
    """Returns an initialized S3 client if credentials exist."""
    if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
        return None
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME,
        endpoint_url=settings.S3_ENDPOINT_URL
    )

def fetch_raw_file_content(document_id: str) -> Optional[str]:
    """Fetches raw file content from S3 given a document ID."""
    s3_client = get_s3_client()
    if not s3_client:
        return "S3 Credentials not configured. Cannot fetch raw file."
        
    try:
        # Assuming document_id maps to an S3 object key
        response = s3_client.get_object(Bucket=settings.S3_BUCKET_NAME, Key=document_id)
        content = response['Body'].read().decode('utf-8')
        return content
    except Exception as e:
        return f"Error fetching {document_id} from S3: {str(e)}"
