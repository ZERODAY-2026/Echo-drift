import requests
from ai.planner import plan
from ai.validator import validate
from ai.explainer import explain
from db.snowflake_client import run_query


def ask(question, history=None):
	out = {"status": "error", "answer": "", "sql": "", "df": None, "records": 0}
	error = None
	for attempt in range(2):  # one automatic retry
		try:
			p = plan(question, history, error)
		except requests.exceptions.ConnectionError:
			out["answer"] = "Cannot reach the AI model. Open the Ollama app (or run 'ollama serve') and try again."
			return out
		except Exception as e:
			out["answer"] = f"AI model error: {e}"
			return out

		status = p.get("status")
		if status in ("ambiguous", "unsupported"):
			out.update(status=status, answer=p.get("message", ""))
			return out

		ok, result = validate(p.get("sql", ""))
		if not ok:
			error = result
			continue

		try:
			df = run_query(result)
		except Exception as e:
			error = str(e)
			continue

		out.update(status="ok", sql=result, df=df, records=len(df),
				   answer=explain(question, result, df))
		return out

	out.update(status="error", answer=f"Could not produce a valid query: {error}")
	return out
