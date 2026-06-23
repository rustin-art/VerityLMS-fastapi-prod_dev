# prompts/assessment_prompts.py

def build_assessment_generation_prompt(
    note_content: str,
    mcq_count: int = 10
):
    """
    Build Assessment Prompt.

    Input:
        Generated Note Content

    Output:
        Structured MCQs JSON
    """

    return f"""
You are an expert instructional designer.

Create {mcq_count} multiple choice questions
based ONLY on the provided notes.

Requirements:

1. Cover all important concepts.
2. One correct answer.
3. Three distractors.
4. Avoid ambiguous questions.
5. Return valid JSON only.

JSON Format:

{{
    "mcq_pool": [
        {{
            "question": "...",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ]
        }}
    ],
    "answers_pool": [
        {{
            "question_number": 1,
            "correct_answer": "A"
        }}
    ]
}}

NOTES:

{note_content}
"""