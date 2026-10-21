
import re
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


PDF_PATH = Path("data/multi_company_employee_handbook.pdf")


# Common heading patterns; no specific company or section numbers required.
NUMBERED_HEADING = re.compile(
    r"^\s*\d+(?:\.\d+)*[.)]?\s+\S.*$"
)

NAMED_HEADING = re.compile(
    r"^\s*(?:chapter|section|part|appendix|annex)"
    r"\s+[\w.-]+(?:\s*[:.\-–—]\s*.*|\s+.*)?$",
    re.IGNORECASE,
)


def is_heading(line):
    """Identify likely headings using common document conventions."""
    line = line.strip()

    if not line or len(line) > 120:
        return False

    if line.endswith((".", "?", "!", ";", ",")):
        return False

    if NUMBERED_HEADING.fullmatch(line):
        return True

    if NAMED_HEADING.fullmatch(line):
        return True

    # Heuristic for short, unnumbered titles such as "Remote Work Policy".
    words = line.split()

    if not 2 <= len(words) <= 10:
        return False

    if not any(char.isalpha() for char in line):
        return False

    capitalised = sum(
        word[0].isupper() or word.isupper()
        for word in words
    )

    return capitalised / len(words) >= 0.7


def split_page_into_sections(page):
    """Split one PDF page at detected headings and retain its metadata."""
    lines = page.page_content.splitlines()

    sections = []
    current_lines = []
    current_heading = "Unlabelled section"

    for line in lines:
        stripped = line.strip()

        if is_heading(stripped):
            # Save the preceding section before starting another.
            existing_text = "\n".join(current_lines).strip()

            if existing_text:
                sections.append(
                    Document(
                        page_content=existing_text,
                        metadata={
                            **page.metadata,
                            "section": current_heading,
                        },
                    )
                )

            current_heading = stripped
            current_lines = [stripped]
        else:
            current_lines.append(line)

    # Save the final section on this page.
    final_text = "\n".join(current_lines).strip()

    if final_text:
        sections.append(
            Document(
                page_content=final_text,
                metadata={
                    **page.metadata,
                    "section": current_heading,
                },
            )
        )

    return sections


def load_and_split_pdf():
    """Load the PDF, split into sections, then create searchable chunks."""
    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"PDF not found at: {PDF_PATH.resolve()}"
        )

    pages = PyPDFLoader(str(PDF_PATH)).load()

    section_documents = []

    for page in pages:
        section_documents.extend(split_page_into_sections(page))

    chunk_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=True,
    )

    chunks = chunk_splitter.split_documents(section_documents)

    for chunk in chunks:
        page_index = chunk.metadata.get("page", 0)

        # Keep both LangChain's zero-based page and a display-ready number.
        chunk.metadata["page_number"] = page_index + 1
        chunk.metadata["source"] = str(PDF_PATH)

        if not chunk.metadata.get("section"):
            chunk.metadata["section"] = "Unlabelled section"

    return chunks


if __name__ == "__main__":
    documents = load_and_split_pdf()

    print(f"Pages loaded: {len(set(doc.metadata['page'] for doc in documents))}")
    print(f"Chunks created: {len(documents)}")
    print("\nFirst 15 chunks:\n")

    for index, doc in enumerate(documents[:15], start=1):
        print("-" * 60)
        print(f"Chunk: {index}")
        print(f"Page: {doc.metadata.get('page_number')}")
        print(f"Section: {doc.metadata.get('section')}")
        print(f"Text: {doc.page_content[:200]}")
