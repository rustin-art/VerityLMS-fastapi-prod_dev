import json
import re

from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.homework import HomeworkModel

from ..schemas.homework import (
    HomeworkCreate,
    HomeworkUpdate
)

from .ai_client import generate_response

from ..prompts.homework_generation_prompt import (
    build_homework_generation_prompt
)
from ..prompts.homework_prompt import build_homework_prompt


# -----------------------------
# Create Homework
# -----------------------------
def create_homework(
    db: Session,
    homework: HomeworkCreate
):

    db_homework = HomeworkModel(
        title=homework.title,
        chapter_id=homework.chapter_id,
        lesson_id=homework.lesson_id,
        homework_questions=homework.homework_questions
    )

    db.add(db_homework)
    db.commit()
    db.refresh(db_homework)

    return db_homework


# -----------------------------
# Get Homework
# -----------------------------
def get_homeworks(
    db: Session,
    homework_id: Optional[int] = None,
    title: Optional[str] = None,
    chapter_id: Optional[int] = None,
    lesson_id: Optional[int] = None,
    published: Optional[bool] = None
):

    query = db.query(
        HomeworkModel
    )

    if homework_id is not None:
        query = query.filter(
            HomeworkModel.id == homework_id
        )

    if title is not None:
        query = query.filter(
            HomeworkModel.title.ilike(
                f"%{title}%"
            )
        )

    if chapter_id is not None:
        query = query.filter(
            HomeworkModel.chapter_id == chapter_id
        )

    if lesson_id is not None:
        query = query.filter(
            HomeworkModel.lesson_id == lesson_id
        )

    if published is not None:
        query = query.filter(
            HomeworkModel.published == published
        )

    results = query.all()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No homework found"
        )

    return results


# -----------------------------
# Get All Homework
# -----------------------------
def get_all_homeworks(
    db: Session
):

    return db.query(
        HomeworkModel
    ).all()


# -----------------------------
# Update Homework
# -----------------------------
def update_homework(
    db: Session,
    homework_id: int,
    homework: HomeworkUpdate
):

    db_homework = db.query(
        HomeworkModel
    ).filter(
        HomeworkModel.id == homework_id
    ).first()

    if not db_homework:
        raise HTTPException(
            status_code=404,
            detail="Homework not found"
        )

    update_data = homework.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            db_homework,
            field,
            value
        )

    db.commit()
    db.refresh(db_homework)

    return db_homework


# -----------------------------
# Delete Homework
# -----------------------------
def delete_homework(
    db: Session,
    homework_id: int
):

    db_homework = db.query(
        HomeworkModel
    ).filter(
        HomeworkModel.id == homework_id
    ).first()

    if not db_homework:
        raise HTTPException(
            status_code=404,
            detail="Homework not found"
        )

    db.delete(db_homework)
    db.commit()

    return {
        "message": "Homework deleted successfully"
    }


# -----------------------------
# Generate Homework
# -----------------------------
def generate_homework(
    goal: str
):

    prompt = build_homework_prompt(
        goal
    )

    content = generate_response(
        prompt=prompt,
        max_tokens=1500,
        temperature=0.3
    )

    content = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    content = re.sub(
        r'[\x00-\x1F\x7F]',
        '',
        content
    )

    try:
        decoder = json.JSONDecoder()

        homework_data, _ = decoder.raw_decode(
            content
        )

    except json.JSONDecodeError:

        fixed_content = content.replace(
            "\\",
            "\\\\"
        )

        decoder = json.JSONDecoder()

        homework_data, _ = decoder.raw_decode(
            fixed_content
        )

    if isinstance(homework_data, list):
        homework_data = homework_data[0]

    return homework_data


# -----------------------------
# Generate & Save Homework
# -----------------------------
def generate_and_save_homework(
    db: Session,
    goal: str
):

    generated_homework = generate_homework(
        goal
    )

    db_homework = HomeworkModel(
        title=generated_homework["title"],
        chapter_id=generated_homework["chapter_id"],
        lesson_id=generated_homework["lesson_id"],
        homework_questions=generated_homework["homework_questions"]
    )

    db.add(db_homework)

    db.commit()

    db.refresh(db_homework)

    return db_homework

# -----------------------------
# Generate Homework from Notes
# -----------------------------

# services/homework_service.py
def generate_homework_from_notes(
    note_content: str,
    question_count: int = 5
):
    """
    Generate Homework
    from Note Content.
    """

    prompt = build_homework_generation_prompt(
        note_content=note_content,
        question_count=question_count
    )

    response = generate_response(
        prompt=prompt,
        max_tokens=3000,
        temperature=0.4
    )

    parsed = json.loads(response)

    return {
        "questions": parsed["questions"],
        "prompt": prompt
    }