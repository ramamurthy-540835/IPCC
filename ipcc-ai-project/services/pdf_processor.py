import fitz  # PyMuPDF


def extract_pdf_text(pdf_path):
    """
    Extract text page by page from a PDF.
    Returns a list of dictionaries:
    [
        {
            "page": 1,
            "content": "..."
        },
        ...
    ]
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_number in range(len(document)):
        page = document.load_page(page_number)

        text = page.get_text("text")

        pages.append({
            "page": page_number + 1,
            "content": text
        })

    document.close()

    return pages