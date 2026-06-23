# models/cleaned_document.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class CleanedDocumentModel(Base):
    __tablename__ = "cleaned_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # FIX: reference correct PK column
    document_id = Column(
        Integer,
        ForeignKey("extracted_documents.document_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    document_name = Column(String, nullable=False)

    extraction_type = Column(String, nullable=False)

    cleaned_text = Column(Text, nullable=False)

    status = Column(String, nullable=False, default="completed")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "extraction_type",
            name="uq_cleaned_document"
        ),
    )