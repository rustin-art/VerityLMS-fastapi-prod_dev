def build_assessment_prompt(goal: str):

    return f"""
    Goal: {goal}

    Generate an educational assessment in JSON format.

    Requirements:
    - Create 5 MCQs
    - Each MCQ should have:
      - question
      - 4 options
      - correct answer

    Return ONLY valid JSON in this format:

    {{
      "title": "Assessment Title",
      "chapter_id": 1,
      "lesson_id": 1,
      "mcq_batch": 5,
      "mcq_pool": [
        {{
          "question": "...",
          "options": ["A", "B", "C", "D"]
        }}
      ],
      "answers_pool": [
        {{
          "question": "...",
          "answer": "..."
        }}
      ]
    }}
    """