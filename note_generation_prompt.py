# This Prompt is being used for Extracted_documents ->context + goal -> generated_notes

def build_note_generation_prompt(
    goal: str,
    context: str
):

    return f"""
You are an expert educator.

GOAL:
{goal}

DOCUMENT CONTENT:
{context}

Instructions:

1. Read document carefully.
2. Generate structured study notes.
3. Use markdown headings.
4. Explain concepts simply.
5. Use bullet points.
6. Keep factual accuracy.
7. Do not hallucinate.
8. Use only information from document.

Generate notes now.
"""