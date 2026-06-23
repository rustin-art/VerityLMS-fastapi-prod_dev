from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    DateTime
)

from sqlalchemy.sql import func

from ..database import Base


class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(String)

    status = Column(
        String,
        default="queued"
    )

    stage = Column(
        String,
        default="uploaded"
    )

    result = Column(
        JSON,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )