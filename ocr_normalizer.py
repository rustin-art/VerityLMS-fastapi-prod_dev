import json
from typing import Any


def normalize_ocr_output(raw: Any) -> list[dict]:
    """
    Convert OpenOCR/OpenRec output into:

    [
        {
            "text": "...",
            "confidence": 0.99,
            "box": [...]
        }
    ]
    """

    normalized = []

    if isinstance(raw, tuple):
        raw = raw[0]

    if not isinstance(raw, list):
        return normalized

    if not raw:
        return normalized

    first = raw[0]

    if isinstance(first, str) and "\t[" in first:

        try:

            json_part = first.split("\t", 1)[1]

            records = json.loads(json_part)

            for record in records:

                text = record.get("transcription", "").strip()

                if not text:
                    continue

                normalized.append(
                    {
                        "text": text,
                        "confidence": record.get("score", 0),
                        "box": record.get("points", [])
                    }
                )

        except Exception:
            return []

    elif isinstance(first, dict):

        for record in raw:

            normalized.append(
                {
                    "text": record.get(
                        "text",
                        record.get("transcription", "")
                    ),
                    "confidence": record.get(
                        "confidence",
                        record.get("score", 0)
                    ),
                    "box": record.get(
                        "box",
                        record.get("points", [])
                    )
                }
            )

    return normalized