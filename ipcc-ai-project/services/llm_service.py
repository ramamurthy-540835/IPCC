import re

import vertexai
from vertexai.generative_models import GenerativeModel

from config import PROJECT_ID, LOCATION, GEMINI_MODEL
from services.prompt_loader import load_prompt
from services.retrieval_service import retrieve_context
from services.document_service import get_documents

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
)

model = GenerativeModel(GEMINI_MODEL)

qa_prompt = load_prompt("qa_prompt.txt")


def build_context(contexts):
    context_text = ""

    for i, item in enumerate(contexts, start=1):
        context_text += (
            f"\nSource {i}\n"
            f"Document: {item['document']}\n"
            f"Chunk: {item['chunk']}\n\n"
            f"{item['content']}\n\n"
        )

    return context_text


def ask_question_with_sources(question: str):
    if re.search(
        r"\bhow many\s+(numbered\s+)?chapters?\b",
        question,
        re.IGNORECASE,
    ):
        documents = get_documents()
        chapters = [
            document
            for document in documents
            if re.search(
                r"Chapter-[0-9]+",
                document["real"],
                re.IGNORECASE,
            )
        ]
        answer = (
            f"The IPCC Cities library contains {len(chapters)} numbered "
            f"chapters: Chapters 1–{len(chapters)}. It also includes "
            "supporting reports such as the Technical Summary, Summary for "
            "Policymakers, and Annex I Glossary."
        )
        sources = [
            {
                "document": document["display"],
                "chunk": "catalog",
                "distance": 0,
                "content": "Document catalog entry",
            }
            for document in chapters
        ]
        return answer, sources

    contexts = retrieve_context(question)

    context_text = build_context(contexts)

    prompt = (
        qa_prompt
        .replace("{context}", context_text)
        .replace("{question}", question)
    )

    response = model.generate_content(prompt)

    return response.text, contexts


def ask_question(question: str):
    answer, _ = ask_question_with_sources(question)
    return answer
