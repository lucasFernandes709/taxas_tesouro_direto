import os
import shutil
import requests
import boto3
import logging
from dotenv import load_dotenv, find_dotenv
from io import BytesIO
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from zipfile import ZipFile


def get_filename(url):
    return os.path.basename(url)[:-4]


def download_csv(url):
    """Download CSV file from a URL."""
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP request errors
    logging.info('CSV file downloaded successfully.')

    return BytesIO(response.content)


def download_and_extract_zip(url, extract_to='./extracted_files/'):
    """Download ZIP compressed file from a URL and extracts its contents."""

    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP request errors
    logging.info('ZIP file file downloaded successfully.')
    zip_file = BytesIO(response.content)

    # Extract gzip file contents
    logging.info(f'Extracting downloaded file to {extract_to} directory.')
    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(path=extract_to)
        extracted_files = zip_ref.namelist()

    # Get extracted files full path
    extracted_files = [os.path.join(extract_to, f) for f in extracted_files]
    logging.info(f"File '{extracted_files[0]}' successfully extracted.")

    return extracted_files


def upload_to_s3(file_obj, bucket_name, object_name):
    """Upload file object to S3 bucket."""
    s3 = boto3.client('s3') # Credentials loaded from environment variables
    try:
        logging.info(f"Uploading file '{object_name}' to s3 bucket '{bucket_name}'")
        s3.upload_fileobj(file_obj, bucket_name, object_name)
        logging.info(f"'{object_name}' file uploaded successfully to s3 bucket '{bucket_name}'.")
    except NoCredentialsError:
        print("Credentials not available.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():

    # Setup logging config
    logging.basicConfig(filename='ingestion_log.log', level=logging.INFO)

    # Load environment variables
    load_dotenv(find_dotenv())
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

    # Download CSV file
    CSV_URL = 'https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv')
    csv_filename = get_filename(CSV_URL)
    logging.info(f"Downloading csv file '{csv_filename}'...")
    csv_obj = download_csv(CSV_URL)
    upload_to_s3(csv_obj, S3_BUCKET_NAME, f'{csv_filename}.csv')

    # Download ZIP file
    ZIP_URLS = [
        'https://www.tesourotransparente.gov.br/ckan/dataset/48a7fd9d-78e5-43cb-bcba-6e7dcaf2d741/resource/96948ba0-60ff-4c2c-b72a-0efbc37fcb23/download/InvestidoresTesouroDiretoate2017.zip',
        'https://www.tesourotransparente.gov.br/ckan/dataset/48a7fd9d-78e5-43cb-bcba-6e7dcaf2d741/resource/6962ca94-38a1-4066-a1a3-bed4a9272644/download/InvestidoresTesouroDireto2018.zip',
        'https://www.tesourotransparente.gov.br/ckan/dataset/48a7fd9d-78e5-43cb-bcba-6e7dcaf2d741/resource/1257e9cd-b434-4bce-b181-95670b46b1a8/download/InvestidoresTesouroDireto2019.zip',
        'https://www.tesourotransparente.gov.br/ckan/dataset/48a7fd9d-78e5-43cb-bcba-6e7dcaf2d741/resource/057eaf94-12e7-41e3-a480-869b5fb9d3ac/download/InvestidoresTesouroDireto2020.zip',
        'https://www.tesourotransparente.gov.br/ckan/dataset/48a7fd9d-78e5-43cb-bcba-6e7dcaf2d741/resource/26e4fd5d-d46b-44f9-948c-3235be81a596/download/InvestidoresTesouroDireto2021.zip',
        'https://www.tesourotransparente.gov.br/ckan/dataset/48a7fd9d-78e5-43cb-bcba-6e7dcaf2d741/resource/ea4d0f68-88ea-4bec-9b96-ea991273b0fd/download/InvestidoresTesouroDireto2022.zip',
        'https://www.tesourotransparente.gov.br/ckan/dataset/48a7fd9d-78e5-43cb-bcba-6e7dcaf2d741/resource/7ae294e2-fc61-4764-add8-6001662b30eb/download/InvestidoresTesouroDireto2023.zip',
        'https://www.tesourotransparente.gov.br/ckan/dataset/48a7fd9d-78e5-43cb-bcba-6e7dcaf2d741/resource/85958d35-45a6-489e-b664-2a8287de0b24/download/InvestidoresTesouroDireto2024.zip'
    ]

    for zip_url in ZIP_URLS:

        zip_filename = get_filename(zip_url)
        extracted_file = download_and_extract_zip(zip_url)[0]
        upload_to_s3(extracted_file, S3_BUCKET_NAME, f'{zip_filename}.csv')

    # Remove all extracted files
    logging.info('Removing temporary extracted files')
    shutil.rmtree('./extracted_files/')


if __name__ == '__main__':
    main()
