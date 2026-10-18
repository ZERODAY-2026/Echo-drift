import re

import sqlglot
from sqlglot import exp


ALLOWED_TABLES = {
	"MACHINES",
	"PRODUCTS",
	"SUPPLIERS",
	"INVENTORY",
	"DOWNTIME",
	"PRODUCTION",
	"ORDERS",
	"DEFECTS",
}
BLOCKED = re.compile(
	r"\b(DROP|DELETE|UPDATE|INSERT|ALTER|TRUNCATE|CREATE|MERGE|GRANT|REVOKE|COPY|CALL|PUT|REMOVE)\b",
	re.I,
)


def validate(sql):
	"""Returns (ok, cleaned_sql_or_error)."""
	sql = (sql or "").strip()
	sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
	sql = re.sub(r"--[^\n]*", " ", sql)
	sql = sql.strip().rstrip(";").strip()
	if not sql:
		return False, "Empty query."
	if ";" in sql:
		return False, "Multiple statements are not allowed."
	if BLOCKED.search(sql):
		return False, "Only read-only SELECT queries are allowed."
	try:
		tree = sqlglot.parse_one(sql, read="snowflake")
	except Exception as e:
		return False, f"SQL syntax error: {e}"
	if tree is None or tree.find(exp.Select) is None:
		return False, "Only SELECT queries are allowed."
	if isinstance(tree, (exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Create, exp.Command)):
		return False, "Only SELECT queries are allowed."
	ctes = {cte.alias.upper() for cte in tree.find_all(exp.CTE)}
	for table in tree.find_all(exp.Table):
		name = (table.name or "").upper()
		if name and name not in ALLOWED_TABLES and name not in ctes:
			return False, f"Unknown table: {table.name}"
	if not tree.args.get("limit"):
		sql += " LIMIT 100"
	return True, sql
