# services/note_lookup_service.py

from sqlalchemy.orm import Session

from ..models.note import NoteModel


def get_note_by_id(
    db: Session,
    note_id: int
) -> NoteModel:

    note = (
        db.query(NoteModel)
        .filter(NoteModel.id == note_id)
        .first()
    )

    if not note:
        raise ValueError(
            f"Note {note_id} not found"
        )

    return note


def note_exists(
    db: Session,
    note_id: int
) -> bool:

    return (
        db.query(NoteModel.id)
        .filter(NoteModel.id == note_id)
        .first()
        is not None
    )


def get_note_content(
    db: Session,
    note_id: int
) -> str:

    note = get_note_by_id(
        db,
        note_id
    )

    return note.content