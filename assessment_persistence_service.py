# services/assessment_persistence_service.py

from ..models.assessment import (
    AssessmentModel
)


def save_assessment(
    db,
    note_id,
    title,
    chapter_id,
    lesson_id,
    mcq_pool,
    answers_pool,
    prompt
):

    assessment = AssessmentModel(
        title=title,

        note_id = note_id,

        chapter_id=chapter_id,

        lesson_id=lesson_id,

        mcq_batch=len(mcq_pool),

        mcq_pool=mcq_pool,

        answers_pool=answers_pool,

        source_prompt=prompt,

        model_used="Mistral-V2"
    )
    print("<!---- Adding assessment created via Pipeline ----!>")
    db.add(assessment)
    print("<!---- Committing Assessment created via Pipeline ----!>")
    db.commit()
    print("<!---- Refreshing Assessment Table ----!>")
    db.refresh(assessment)

    return assessment