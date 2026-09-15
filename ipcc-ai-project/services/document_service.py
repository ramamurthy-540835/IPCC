import base64
from google.cloud import bigquery, storage

from config import (
    PROJECT_ID,
    DATASET_ID,
    DOCUMENTS_TABLE,
    BUCKET_NAME,
)

bigquery_client = bigquery.Client(project=PROJECT_ID)
storage_client = storage.Client(project=PROJECT_ID)

DOCUMENTS = f"{PROJECT_ID}.{DATASET_ID}.{DOCUMENTS_TABLE}"


def clean_name(name: str) -> str:
    name = name.replace("srcities_sod_", "")
    name = name.replace("_ramamurthy.valavandan.pdf", "")
    name = name.replace(".pdf", "")
    name = name.replace("---", " — ")
    name = name.replace("-", " ")
    return name.strip()


def get_documents():
    query = f"""
    SELECT
        document_name,
        COUNT(*) AS chunks
    FROM `{DOCUMENTS}`
    GROUP BY document_name
    ORDER BY document_name
    """

    rows = bigquery_client.query(query).result()

    bucket = storage_client.bucket(BUCKET_NAME)

    documents = []

    for row in rows:
        blob = bucket.blob(row.document_name)
        blob.reload()

        documents.append({
            "real": row.document_name,
            "display": clean_name(row.document_name),
            "chunks": row.chunks,
            "size_mb": round(blob.size / (1024 * 1024), 2),
        })

    return documents


def get_document_text(document_name: str):
    query = f"""
    SELECT content
    FROM `{DOCUMENTS}`
    WHERE document_name=@document_name
    ORDER BY chunk_index
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "document_name",
                "STRING",
                document_name,
            )
        ]
    )

    rows = bigquery_client.query(
        query,
        job_config=job_config,
    ).result()

    return "\n".join(row.content for row in rows)


def get_pdf_base64(document_name: str):
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(document_name)

    pdf_bytes = blob.download_as_bytes()

    return base64.b64encode(pdf_bytes).decode("utf-8")