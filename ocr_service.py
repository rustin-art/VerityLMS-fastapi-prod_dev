import json
import logging

from ..core.openocr_manager import ocr_manager
from ..services.file_validator import validate_image_path

logger = logging.getLogger(__name__)


def run_ocr(image_path: str):
    """
    Execute OCR.

    Returns normalized OCR blocks:

    [
        {
            "text": "...",
            "bbox": [...],
            "confidence": 0.99
        }
    ]
    """

    image_path = validate_image_path(image_path)

    result = ocr_manager.ocr(image_path=image_path)

    cleaned = []

    if not isinstance(result, tuple):
        logger.warning("Unexpected OCR result type: %s", type(result))
        return cleaned

    result_lines = result[0]

    for line in result_lines:

        try:

            _, json_part = line.split("\t", 1)

            records = json.loads(json_part)

            for item in records:

                text = item.get("transcription", "").strip()

                if not text:
                    continue

                cleaned.append(
                    {
                        "text": text,
                        "bbox": item.get("points", []),
                        "confidence": item.get("score", 0.0)
                    }
                )

        except Exception:
            logger.exception("OCR parse failure")

    logger.info(
        "OCR extracted %s text blocks",
        len(cleaned)
    )

    return cleaned