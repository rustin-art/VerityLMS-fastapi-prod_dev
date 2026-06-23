import json

from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.assessment import AssessmentModel
from ..schemas.assessment import (
    AssessmentCreate,
    AssessmentUpdate
)

from .ai_client import generate_response

from ..prompts.assessment_generation_prompt import (
    build_assessment_generation_prompt
)
from ..prompts.assessment_prompt import build_assessment_prompt


# -----------------------------
# Create Assessment
# -----------------------------
def create_assessment(
    db: Session,
    assessment: AssessmentCreate
):

    db_assessment = AssessmentModel(
        title=assessment.title,
        chapter_id=assessment.chapter_id,
        lesson_id=assessment.lesson_id,
        mcq_batch=assessment.mcq_batch,
        mcq_pool=assessment.mcq_pool,
        answers_pool=assessment.answers_pool
    )

    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)

    return db_assessment


# -----------------------------
# Get Assessment(s)
# -----------------------------
def get_assessments(
    db: Session,
    assessment_id: Optional[int] = None,
    title: Optional[str] = None,
    chapter_id: Optional[int] = None,
    lesson_id: Optional[int] = None,
    published: Optional[bool] = None,
    mcq_batch: Optional[int] = None
):

    query = db.query(
        AssessmentModel
    )

    if assessment_id is not None:
        query = query.filter(
            AssessmentModel.id == assessment_id
        )

    if title is not None:
        query = query.filter(
            AssessmentModel.title.ilike(
                f"%{title}%"
            )
        )

    if chapter_id is not None:
        query = query.filter(
            AssessmentModel.chapter_id == chapter_id
        )

    if lesson_id is not None:
        query = query.filter(
            AssessmentModel.lesson_id == lesson_id
        )

    if published is not None:
        query = query.filter(
            AssessmentModel.published == published
        )

    if mcq_batch is not None:
        query = query.filter(
            AssessmentModel.mcq_batch == mcq_batch
        )

    results = query.all()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No assessments found"
        )

    return results


# -----------------------------
# Get All Assessments
# -----------------------------
def get_all_assessments(
    db: Session
):

    return db.query(
        AssessmentModel
    ).all()


# -----------------------------
# Update Assessment
# -----------------------------
def update_assessment(
    db: Session,
    assessment_id: int,
    assessment: AssessmentUpdate
):

    db_assessment = db.query(
        AssessmentModel
    ).filter(
        AssessmentModel.id == assessment_id
    ).first()

    if not db_assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )

    update_data = assessment.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            db_assessment,
            field,
            value
        )

    db.commit()
    db.refresh(db_assessment)

    return db_assessment


# -----------------------------
# Delete Assessment
# -----------------------------
def delete_assessment(
    db: Session,
    assessment_id: int
):

    db_assessment = db.query(
        AssessmentModel
    ).filter(
        AssessmentModel.id == assessment_id
    ).first()

    if not db_assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )

    db.delete(db_assessment)
    db.commit()

    return {
        "message": "Assessment deleted successfully"
    }


# -----------------------------
# Generate Assessment
# -----------------------------
def generate_assessment(
    goal: str
):

    prompt = build_assessment_prompt(
        goal
    )

    content = generate_response(
        prompt=prompt,
        max_tokens=1500,
        temperature=0.7
    )

    assessment_data = json.loads(
        content
    )

    return AssessmentCreate(
        title=assessment_data["title"],
        chapter_id=assessment_data["chapter_id"],
        lesson_id=assessment_data["lesson_id"],
        mcq_batch=assessment_data["mcq_batch"],
        mcq_pool=assessment_data["mcq_pool"],
        answers_pool=assessment_data["answers_pool"]
    )


# -----------------------------
# Generate & Save Assessment
# -----------------------------
def generate_and_save_assessment(
    db: Session,
    goal: str
):

    assessment = generate_assessment(
        goal
    )

    db_assessment = AssessmentModel(
        title=assessment.title,
        chapter_id=assessment.chapter_id,
        lesson_id=assessment.lesson_id,
        mcq_batch=assessment.mcq_batch,
        mcq_pool=assessment.mcq_pool,
        answers_pool=assessment.answers_pool
    )

    db.add(db_assessment)

    db.commit()

    db.refresh(db_assessment)

    return db_assessment

# -----------------------------
# Generate Assessment from Notes
# -----------------------------

# services/assessment_service.py

def generate_assessment_from_notes(
    note_content: str,
    mcq_count: int = 10
):
    """
    Generate Assessment
    from Note Content.
    """

    prompt = build_assessment_generation_prompt(
        note_content=note_content,
        mcq_count=mcq_count
    )

    response = generate_response(
        prompt=prompt,
        max_tokens=3000,
        temperature=0.3
    )

    parsed = json.loads(response)

    return {
        "mcq_pool": parsed["mcq_pool"],
        "answers_pool": parsed["answers_pool"],
        "prompt": prompt
    }