import tempfile
from pathlib import Path

from fastapi import UploadFile


async def save_upload(file: UploadFile) -> str:

    suffix = Path(file.filename).suffix

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp:

        content = await file.read()
        temp.write(content)

        return temp.name