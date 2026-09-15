from services.llm_service import model
from services.prompt_loader import load_prompt

summary_prompt = load_prompt("summary_prompt.txt")


def split_text(text: str, chunk_size: int = 6000, max_parts: int = 6):
    text = text[: chunk_size * max_parts]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end

    return chunks


def summarize_document(text: str):
    chunks = split_text(text)

    partial_summaries = []

    for i, chunk in enumerate(chunks, start=1):
        prompt = f"""
Summarize this part of the IPCC document clearly and concisely.

Part {i} of {len(chunks)}

Text:
{chunk}
"""

        response = model.generate_content(prompt)
        partial_summaries.append(response.text)

    combined_summary_text = "\n\n".join(partial_summaries)

    final_prompt = summary_prompt.replace(
        "{text}",
        combined_summary_text,
    )

    final_response = model.generate_content(final_prompt)

    return final_response.text