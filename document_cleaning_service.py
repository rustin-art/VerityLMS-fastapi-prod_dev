# services/document_cleaning_service.py

# =====================================================
# OCR CLEANING
# =====================================================
from typing import Any, List, Dict


def clean_ocr_text(data: dict) -> str:
    """
    Convert OCR JSON into plain text.
    """

    print("<---- Cleaning OCR Data ---->")

    pages = data.get("pages", [])

    cleaned_pages = []

    for page in pages:

        page_lines = []

        for block in page:

            text = (
                block.get("text")
                or block.get("transcription")
                or ""
            )

            text = text.strip()

            if text:
                page_lines.append(text)

        if page_lines:
            cleaned_pages.append(
                "\n".join(page_lines)
            )

    return (
        "\n\n--- PAGE BREAK ---\n\n"
        .join(cleaned_pages)
        .strip()
    )


import json
import logging

logger = logging.getLogger(__name__)


# =====================================================
# INTERNAL TEXT EXTRACTOR
# =====================================================
def unirec_extract_text(value: Any, chunks: List[str]) -> None:
    """
    Recursively extracts text from arbitrary UniRec output.

    Supports:
    - str
    - dict
    - list
    - tuple

    Handles common UniRec/OpenOCR fields:
    - text
    - content
    - markdown
    - transcription
    - value
    - result
    """

    if value is None:
        return

    # ----------------------------------
    # STRING
    # ----------------------------------
    if isinstance(value, str):

        text = value.strip()

        if text:
            chunks.append(text)

        return

    # ----------------------------------
    # DICT
    # ----------------------------------
    if isinstance(value, dict):

        priority_keys = [
            "text",
            "content",
            "markdown",
            "transcription",
            "value"
        ]

        # Extract known text fields first
        found_text = False

        for key in priority_keys:

            field = value.get(key)

            if isinstance(field, str):

                text = field.strip()

                if text:
                    chunks.append(text)
                    found_text = True

        # Continue recursively through all fields
        for nested_value in value.values():

            if isinstance(
                nested_value,
                (dict, list, tuple)
            ):
                unirec_extract_text(
                    nested_value,
                    chunks
                )

        return

    # ----------------------------------
    # LIST
    # ----------------------------------
    if isinstance(value, list):

        for item in value:
            unirec_extract_text(item, chunks)

        return

    # ----------------------------------
    # TUPLE
    # ----------------------------------
    if isinstance(value, tuple):

        for item in value:
            unirec_extract_text(item, chunks)

        return


# =====================================================
# UNIREC CLEANING
# =====================================================
def clean_unirec_text(data: Any) -> str:
    """
    Convert arbitrary UniRec output into
    clean LLM-ready text.

    Production safe:
    - nested structures
    - tuples
    - dicts
    - lists
    - markdown outputs
    - OCR-like outputs
    """

    logger.info("Cleaning UniRec data")

    if data is None:
        return ""

    chunks: List[str] = []

    try:

        unirec_extract_text(
            value=data,
            chunks=chunks
        )

        # Remove empties
        chunks = [
            x.strip()
            for x in chunks
            if x and x.strip()
        ]

        # Remove duplicates while preserving order
        seen = set()
        unique_chunks = []

        for item in chunks:

            if item not in seen:

                seen.add(item)
                unique_chunks.append(item)

        cleaned_text = "\n\n".join(unique_chunks)

        logger.info(
            "UniRec cleaning complete: %s chunks extracted",
            len(unique_chunks)
        )

        return cleaned_text.strip()

    except Exception:

        logger.exception(
            "Failed to clean UniRec output"
        )

        return ""


# =====================================================
# MAIN ENTRY POINT
# =====================================================
def build_clean_text(extraction_type: str, extracted_data: Any) -> str:
    """
    Normalizes extracted data into LLM-ready text.
    """

    if extraction_type == "ocr":
        return clean_ocr_text(extracted_data)

    if extraction_type == "unirec":
        return clean_unirec_text(extracted_data)

    raise ValueError(f"Unsupported extraction type: {extraction_type}")