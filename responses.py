from pydantic import BaseModel
from typing import Any, Optional


class OCRResponse(BaseModel):
    document_id: int

    task: str

    results: Optional[Any] = None
    pages: Optional[Any] = None

    text: Optional[str] = None

    timings: Optional[Any] = None