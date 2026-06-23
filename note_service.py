from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.note import NoteModel

from ..schemas.note import (
    NoteCreate,
    NoteUpdate,
    GoalRequest
)

from .ai_client import generate_response
from ..prompts.note_prompt import build_note_prompt
from ..prompts.note_generation_prompt import (
    build_note_generation_prompt
)


# -----------------------------
# Create Note
# -----------------------------
def create_note(
    db: Session,
    note: NoteCreate
):

    db_note = NoteModel(
        title=note.title,
        chapter_id=note.chapter_id,
        lesson_id=note.lesson_id,
        content=note.content
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


# -----------------------------
# Get Notes
# -----------------------------
def get_notes(
    db: Session,
    notes_id: Optional[int] = None,
    title: Optional[str] = None,
    chapter_id: Optional[int] = None
):

    query = db.query(NoteModel)

    if notes_id is not None:
        query = query.filter(
            NoteModel.id == notes_id   
        )

    if title is not None:
        query = query.filter(
            NoteModel.title.ilike(f"%{title}%")
        )

    if chapter_id is not None:
        query = query.filter(
            NoteModel.chapter_id == chapter_id
        )

    results = query.all()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No notes found"
        )

    return results


# -----------------------------
# Get All Notes
# -----------------------------
def get_all_notes(
    db: Session
):

    return db.query(
        NoteModel
    ).all()


# -----------------------------
# Update Note
# -----------------------------
def update_note(
    db: Session,
    notes_id: int,
    note: NoteUpdate
):

    db_note = db.query(NoteModel).filter(
        NoteModel.id == notes_id   
    ).first()

    if not db_note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    update_data = note.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_note, field, value)

    db.commit()
    db.refresh(db_note)

    return db_note


# -----------------------------
# Delete Note
# -----------------------------
def delete_note(
    db: Session,
    notes_id: int
):

    db_note = db.query(NoteModel).filter(
        NoteModel.id == notes_id   
    ).first()

    if not db_note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    db.delete(db_note)
    db.commit()

    return {
        "message": "Note deleted successfully"
    }

# -----------------------------
# Generate Notes
# -----------------------------
def generate_notes_without_docs(goal: str):

    prompt = build_note_prompt(goal)

    content = generate_response(
        prompt=prompt,
        max_tokens=2000,
        temperature=0.7
    )

    return {
        "title": f"AI Notes: {goal}",
        "chapter_id": 1,
        "lesson_id": 1,
        "content": content,

        # 🔥 AI metadata (NOW INCLUDED)
        "source_prompt": prompt,
        "model_used": "Mistral-V3"
    }


# -----------------------------
# Generate & Save Notes
# -----------------------------
def generate_and_save_notes(
    db: Session,
    goal: str
):

    generated_note = generate_notes_without_docs(goal)

    db_note = NoteModel(
        **generated_note
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note

# -----------------------------
# Re-Generate & Save Notes
# -----------------------------
def regenerate_note(
    db: Session,
    note_id: int
):

    # 1. fetch original note
    db_note = db.query(NoteModel).filter(
        NoteModel.id == note_id
    ).first()

    if not db_note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    # 2. ensure we have a prompt to regenerate
    if not db_note.source_prompt:
        raise HTTPException(
            status_code=400,
            detail="No source prompt found for regeneration"
        )

    # 3. re-run LLM using same prompt
    content = generate_response(
        prompt=db_note.source_prompt,
        max_tokens=2000,
        temperature=0.8  # slight variation for regeneration
    )

    # 4. create NEW note (versioning approach)
    new_note = NoteModel(
        title=f"{db_note.title} (Regenerated)",
        chapter_id=db_note.chapter_id,
        lesson_id=db_note.lesson_id,
        content=content,

        # AI tracking
        source_prompt=db_note.source_prompt,
        model_used=db_note.model_used or "Mistral-V3"
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

# -----------------------------------------------
# Generate Notes From Document Based on Pipeline
# -----------------------------------------------

def generate_notes_from_document(
    goal: str,
    context: str
):

    prompt = build_note_generation_prompt(
        goal=goal,
        context=context
    )

    content = generate_response(
        prompt=prompt,
        max_tokens=5000,
        temperature=0.5
    )

    return {
        "content": content,
        "prompt": prompt
    }