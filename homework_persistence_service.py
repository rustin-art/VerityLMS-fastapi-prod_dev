# services/homework_persistence_service.py

from ..models.homework import (
    HomeworkModel
)


def save_homework(
    db,
    note_id,
    title,
    chapter_id,
    lesson_id,
    homework_questions,
    prompt
):

    homework = HomeworkModel(
        title=title,

        note_id = note_id,

        chapter_id=chapter_id,

        lesson_id=lesson_id,

        homework_questions=homework_questions,

        source_prompt=prompt,

        model_used="Mistral-V2"
    )
    print("<!---- Adding Homework created via Pipeline ----!>")
    db.add(homework)
    print("<!---- Committing Homework created via Pipeline ----!>")
    db.commit()
    print("<!---- Refreshing Homework Table ----!>")
    db.refresh(homework)

    return homework