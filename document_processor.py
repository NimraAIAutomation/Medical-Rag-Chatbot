
import fitz
import re


def extract_pdf(uploaded_file):

    documents = []
    current_section = "Not identified"

    pdf_bytes = uploaded_file.read()
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page_number, page in enumerate(pdf, start=1):

        text = page.get_text("text").strip()

        if not text:
            continue

        lines = text.splitlines()

        for line in lines:
            line = line.strip()

            # Detect common numbered section headings
            if re.match(
                r"^(chapter\s+\d+|section\s+\d+|\d+(\.\d+)*\.?\s+[A-Z])",
                line,
                re.IGNORECASE
            ):
                current_section = line

        documents.append({
            "text": text,
            "metadata": {
                "source": uploaded_file.name,
                "page_number": page_number,
                "section": current_section
            }
        })

    pdf.close()

    return documents
