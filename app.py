import streamlit as st
import plotly.express as px
import pandas as pd
from ai.pipeline import ask
from ai.schema import SCHEMA_TEXT
from db.snowflake_client import run_query

st.set_page_config(page_title="DataMind Manufacturing", page_icon="🏭", layout="wide")
st.title("🏭 DataMind Manufacturing")
st.caption("Ask about your factory in plain English. Every answer comes with proof: the SQL and the raw records.")

EXAMPLES = [
	"Which machine had the most downtime in the last 14 days?",
	"Why were orders delayed?",
	"Which materials are below reorder point?",
	"How is production?",
	"Predict next year's profit",
]
BADGES = {"ok": "✅ Answered with evidence",
		  "ambiguous": "❓ Needs clarification",
		  "unsupported": "🚫 Unsupported, will not guess",
		  "error": "⚠️ Could not complete"}


@st.cache_data(ttl=300)
def get_kpis():
	q = lambda s: run_query(s).iloc[0, 0]
	return (
		round(float(q("SELECT COALESCE(SUM(DURATION_MIN),0)/60 FROM DOWNTIME WHERE START_TIME >= DATEADD(day,-7,CURRENT_DATE())")), 1),
		int(q("SELECT COUNT(*) FROM ORDERS WHERE STATUS='Delayed'")),
		int(q("SELECT COUNT(*) FROM INVENTORY WHERE STOCK_LEVEL < REORDER_POINT")),
	)


def make_chart(df):
	if df is None or df.empty or len(df.columns) < 2 or len(df) > 60:
		return None
	nums = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
	cats = [c for c in df.columns if c not in nums]
	if not nums:
		return None
	x, y = (cats[0] if cats else df.columns[0]), nums[0]
	if x == y:
		return None
	if "date" in x.lower() or "time" in x.lower():
		return px.line(df, x=x, y=y, markers=True)
	return px.bar(df, x=x, y=y)


# Sidebar
with st.sidebar:
	st.header("Connection")
	try:
		run_query("SELECT 1")
		st.success("Snowflake connected")
	except Exception as e:
		st.error(f"Snowflake error: {e}")
	with st.expander("Database schema"):
		st.code(SCHEMA_TEXT.split("Notes:")[0], language="text")
	if st.button("Clear chat"):
		st.session_state.chat = []
		st.rerun()

# KPI header
try:
	dt, delayed, low = get_kpis()
	c1, c2, c3 = st.columns(3)
	c1.metric("Downtime, last 7 days (hrs)", dt)
	c2.metric("Delayed orders", delayed)
	c3.metric("Low-stock materials", low)
except Exception:
	st.warning("KPIs unavailable")

if "chat" not in st.session_state:
	st.session_state.chat = []

# Example buttons
st.write("**Try an example:**")
cols = st.columns(len(EXAMPLES))
clicked = None
for c, q in zip(cols, EXAMPLES):
	if c.button(q, use_container_width=True):
		clicked = q

question = clicked or st.chat_input("Ask a question about production, downtime, inventory, orders or defects...")

if question:
	history = [m["q"] for m in st.session_state.chat]
	with st.spinner("Analysing your data..."):
		res = ask(question, history)
	st.session_state.chat.append({"q": question, "res": res})

# Chat display
for i, m in enumerate(st.session_state.chat):
	with st.chat_message("user"):
		st.write(m["q"])
	res = m["res"]
	with st.chat_message("assistant"):
		st.markdown(f"**{BADGES.get(res['status'], '')}**")
		if res["status"] == "ok":
			st.caption(f"Based on {res['records']} records")
			t1, t2, t3, t4 = st.tabs(["Answer", "SQL", "Data", "Chart"])
			with t1:
				st.write(res["answer"])
			with t2:
				st.code(res["sql"], language="sql")
			with t3:
				st.dataframe(res["df"], use_container_width=True)
				st.download_button("Download CSV", res["df"].to_csv(index=False),
								   file_name="result.csv", key=f"dl{i}")
			with t4:
				fig = make_chart(res["df"])
				if fig:
					st.plotly_chart(fig, use_container_width=True, key=f"ch{i}")
				else:
					st.info("No chart for this result.")
		else:
			st.write(res["answer"])
