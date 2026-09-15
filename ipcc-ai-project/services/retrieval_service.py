from google.cloud import bigquery

from config import (
    PROJECT_ID,
    DATASET_ID,
    DOCUMENTS_TABLE,
)

from services.vector_search import search_documents

client = bigquery.Client(project=PROJECT_ID)

DOCUMENTS = f"{PROJECT_ID}.{DATASET_ID}.{DOCUMENTS_TABLE}"


def retrieve_context(question: str, top_k: int = 5):

    matches = search_documents(question, top_k)

    contexts = []

    for match in matches:

        query = f"""
        SELECT
            content
        FROM `{DOCUMENTS}`
        WHERE id=@id
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(
                    "id",
                    "STRING",
                    match.id,
                )
            ]
        )

        rows = list(
            client.query(
                query,
                job_config=job_config,
            ).result()
        )

        if rows:

            contexts.append({

                "document": match.document_name,

                "chunk": match.chunk_index,

                "distance": match.distance,

                "content": rows[0].content,

            })

    return contexts