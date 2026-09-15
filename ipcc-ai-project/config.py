import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")

DATASET_ID = os.getenv("DATASET_ID")

DOCUMENTS_TABLE = os.getenv("DOCUMENTS_TABLE")
EMBEDDINGS_TABLE = os.getenv("EMBEDDINGS_TABLE")

BUCKET_NAME = os.getenv("BUCKET_NAME")

GEMINI_MODEL = os.getenv("GEMINI_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

TOP_K = int(os.getenv("TOP_K", 5))
EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", 25))