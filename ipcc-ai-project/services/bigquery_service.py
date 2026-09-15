import uuid
from google.cloud import bigquery

from config import DATASET_ID, DOCUMENTS_TABLE, PROJECT_ID

client = bigquery.Client(project=PROJECT_ID)

TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{DOCUMENTS_TABLE}"


def insert_chunks(document_name, page_number, chunks):
    rows = []

    for index, chunk in enumerate(chunks):
        rows.append({
            "id": str(uuid.uuid4()),
            "document_name": document_name,
            "page": page_number,
            "chunk_index": index + 1,
            "content": chunk
        })

    try:
        errors = client.insert_rows_json(TABLE_ID, rows)

        if errors:
            print("BigQuery Errors:")
            print(errors)
        else:
            print(f"Inserted page {page_number}")

    except Exception as e:
        print("Exception:")
        print(type(e).__name__)
        print(e)
        raise
