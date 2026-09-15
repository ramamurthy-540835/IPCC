from services.llm_service import model
from services.prompt_loader import load_prompt

improvement_prompt = load_prompt("improvement_prompt.txt")


def trim_text(text: str, max_chars: int = 36000):
    return text[:max_chars]


def improve_document(text: str):
    text = trim_text(text)

    prompt = improvement_prompt.replace(
        "{text}",
        text,
    )

    response = model.generate_content(prompt)

    return response.text