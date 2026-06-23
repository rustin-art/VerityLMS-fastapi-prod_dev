def build_homework_prompt(goal: str):

    return f"""
    Goal: {goal}

You are a strict JSON generator.

CRITICAL RULES:
- Return ONLY a single JSON object (NOT an array)
- Do NOT include markdown
- Do NOT include explanations
- Do NOT include notes
- Do NOT include any text outside JSON
- Do NOT wrap output in ``` or ```json
- Do NOT return a list/array at top level

You will be penalized for invalid JSON.

Generate exactly 5 homework questions.

Each question must contain:
- question (string)

Return ONLY valid JSON in this format:

{{
  "title": "Homework Title",
  "chapter_id": 1,
  "lesson_id": 1,
  "homework_questions": [
    {{
      "question": "..."
    }}
  ]
}}
"""