from pathlib import Path

## this validation is for valid file paths before pipeline starts
def validate_image_path(path: str):
    p = Path(path)

    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if p.stat().st_size == 0:
        raise ValueError("Empty file")

    return str(p)