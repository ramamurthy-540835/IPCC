from google.cloud import bigquery

from config import (
    PROJECT_ID,
    DATASET_ID,
    DOCUMENTS_TABLE,
    EMBEDDINGS_TABLE,
)

from services.embedding_service import get_embedding

client = bigquery.Client(project=PROJECT_ID)

DOCUMENTS = f"{PROJECT_ID}.{DATASET_ID}.{DOCUMENTS_TABLE}"
EMBEDDINGS = f"{PROJECT_ID}.{DATASET_ID}.{EMBEDDINGS_TABLE}"


def search_documents(question: str, top_k: int = 5):

    query_embedding = get_embedding(question)

    query = f"""
    SELECT
        base.id,
        base.document_name,
        base.chunk_index,
        distance
    FROM VECTOR_SEARCH(
        TABLE `{EMBEDDINGS}`,
        'embedding',
        (
            SELECT
                @embedding AS embedding
        ),
        top_k => {top_k},
        distance_type => 'COSINE'
    )
    ORDER BY distance
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ArrayQueryParameter(
                "embedding",
                "FLOAT64",
                query_embedding,
            )
        ]
    )

    return client.query(
        query,
        job_config=job_config,
    ).result()