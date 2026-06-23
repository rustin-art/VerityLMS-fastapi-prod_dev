# services/note_persistence_service.py

from ..models.note import NoteModel


def save_note(
    db,
    *,
    document_id,
    title,
    chapter_id,
    lesson_id,
    goal,
    content,
    prompt
):
    """
    This Function is to commit Note created from Extracted_data->LLM->Notes
    which will be used as a service for the Note Creation Pipeline
    """

    note = NoteModel(
        document_id=document_id,
        title=title,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        goal=goal,
        content=content,
        source_prompt=prompt,
        model_used="Mistral-V2"
    )
    print("<!---- Adding Note created via Pipeline ----!>")
    db.add(note)
    print("<!---- Committing Note created via Pipeline ----!>")
    db.commit()
    print("<!---- Refreshing Note Table ----!>")
    db.refresh(note)

    return note