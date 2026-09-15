import vertexai
from vertexai.language_models import TextEmbeddingModel

from config import (
    PROJECT_ID,
    LOCATION,
    EMBEDDING_MODEL,
)

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
)

model = TextEmbeddingModel.from_pretrained(
    EMBEDDING_MODEL
)


def get_embedding(text: str):

    response = model.get_embeddings([text])

    return response[0].values


def get_embeddings(texts: list[str]):

    response = model.get_embeddings(texts)

    return [x.values for x in response]