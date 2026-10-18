import os
import json

import requests

from ai.schema import SCHEMA_TEXT, EXAMPLES


MODEL = os.getenv("OLLAMA_MODEL", "gemma4:31b-cloud")

SYSTEM = f"""You convert factory manager questions into Snowflake SQL.
{SCHEMA_TEXT}
Reply with ONLY JSON: {{"status":"ok|ambiguous|unsupported","sql":"...","message":"..."}}
- ok: write one SELECT query using only the tables and columns above.
- ambiguous: the question is too vague; put a clarifying question in message.
- unsupported: the data cannot answer it; explain why in message. Never guess.
Examples:
{EXAMPLES}"""


def _parse(text):
    text = (text or "").strip()
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.lower().startswith("json"):
            text = text[4:]
    try:
        return json.loads(text)
    except Exception:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            return json.loads(text[start:end + 1])
        raise


def plan(question, history=None, error=None):
    messages = [{"role": "system", "content": SYSTEM}]
    for previous_question in (history or [])[-3:]:
        messages.append({"role": "user", "content": previous_question})

    user_message = question
    if error:
        user_message += f"\n\nYour previous SQL failed with: {error}\nReturn corrected JSON."
    messages.append({"role": "user", "content": user_message})

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0},
        },
        timeout=180,
    )
    response.raise_for_status()

    try:
        return _parse(response.json()["message"]["content"])
    except Exception:
        return {"status": "ok", "sql": "", "message": "Model returned invalid JSON"}