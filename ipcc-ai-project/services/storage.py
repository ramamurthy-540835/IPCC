from google.cloud import storage
import os

from config import BUCKET_NAME, PROJECT_ID

client = storage.Client(project=PROJECT_ID)


def list_pdfs():
    bucket = client.bucket(BUCKET_NAME)

    return [blob.name for blob in bucket.list_blobs()
            if blob.name.endswith(".pdf")]


def download_pdf(blob_name):
    bucket = client.bucket(BUCKET_NAME)

    blob = bucket.blob(blob_name)

    os.makedirs("downloads", exist_ok=True)

    destination = os.path.join("downloads", os.path.basename(blob_name))

    blob.download_to_filename(destination)

    return destination
