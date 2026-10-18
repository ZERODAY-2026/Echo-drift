import os

import requests

MODEL = os.getenv("OLLAMA_MODEL", "gemma4:31b-cloud")


def explain(question, sql, df):
    if df.empty:
        return "The query ran but returned no records, so there is no evidence to answer this."

    fallback = f"The query returned {len(df)} record(s). See the Data tab for the evidence."
    prompt = (
        f"Question: {question}\nSQL: {sql}\nRows ({len(df)} total, first 20):\n"
        f"{df.head(20).to_string(index=False)}\n\n"
        "Answer in 2-4 plain sentences for a factory manager. Use ONLY the numbers in the rows. "
        "Do not invent causes that the data does not show. Mention the record count."
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2},
            },
            timeout=180,
        )
        response.raise_for_status()
        text = response.json().get("response", "").strip()
        return text or fallback
    except Exception:
        return fallback