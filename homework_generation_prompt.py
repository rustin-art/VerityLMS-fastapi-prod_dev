# prompts/homework_prompts.py

def build_homework_generation_prompt(
    note_content: str,
    question_count: int = 5
):
    """
    Build Homework Prompt.

    Input:
        Generated Note Content

    Output:
        Homework JSON
    """

    return f"""
You are an expert teacher.

Create {question_count} homework questions
based ONLY on the provided notes.

Requirements:

1. Encourage critical thinking.
2. Mix short-answer and descriptive questions.
3. Cover key concepts.
4. Return JSON only.

JSON Format:

{{
    "questions": [
        {{
            "question": "..."
        }}
    ]
}}

NOTES:

{note_content}
"""