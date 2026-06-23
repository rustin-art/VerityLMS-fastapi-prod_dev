def format_ocr_results(results):
    items = []

    if not isinstance(results, list):
        return []

    for line in results:

        if not isinstance(line, dict):
            continue

        text = (line.get("text") or line.get("transcription") or "").strip()

        if not text:
            continue

        items.append({
            "box": line.get("bbox") or line.get("points") or [],
            "text": text,
            "confidence": float(line.get("score") or 0.0)
        })

    return items


def build_plain_text(items):
    """
    Safe OCR text builder (handles missing/empty bbox)
    """

    if not items:
        return ""

    def sort_key(item):
        box = item.get("box") or item.get("bbox") or []

        try:
            if len(box) > 0 and isinstance(box[0], (list, tuple)):
                return min(p[1] for p in box if len(p) > 1)
        except Exception:
            pass

        return 0

    sorted_items = sorted(items, key=sort_key)

    texts = []

    for item in sorted_items:
        text = (item.get("text") or "").strip()
        if text:
            texts.append(text)

    return "\n".join(texts)