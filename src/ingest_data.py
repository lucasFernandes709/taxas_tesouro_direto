import os
import requests
import boto3
from dotenv import load_dotenv, find_dotenv
from io import BytesIO
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def download_csv(url):
    """Download CSV file from a URL."""
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP request errors
    return BytesIO(response.content)


def upload_to_s3(file_obj, bucket_name, object_name):
    """Upload file object to S3 bucket."""
    s3 = boto3.client('s3') # Credentials loaded from environment variables
    try:
        s3.upload_fileobj(file_obj, bucket_name, object_name)
        print(f"File uploaded successfully to bucket '{bucket_name}' with object name '{object_name}'.")
    except NoCredentialsError:
        print("Credentials not available.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    
    load_dotenv(find_dotenv())

    # Download CSV file
    CSV_URL = 'https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv'
    file_obj = download_csv(CSV_URL)
    
    # Upload to S3
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    S3_OBJECT_NAME = os.getenv('S3_OBJECT_NAME')

    upload_to_s3(file_obj, S3_BUCKET_NAME, S3_OBJECT_NAME)


if __name__ == '__main__':
    main()
