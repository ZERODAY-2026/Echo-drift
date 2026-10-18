import os
import warnings

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv(encoding="utf-8-sig")

_conn = None


def get_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        client_session_keep_alive=True,
    )


def _shared():
    global _conn
    if _conn is None or _conn.is_closed():
        _conn = get_connection()
    return _conn


def _clean(df):
    for c in df.columns:
        try:
            df[c] = pd.to_numeric(df[c])
        except (ValueError, TypeError):
            pass
    return df


def run_query(sql):
    cur = _shared().cursor()
    try:
        cur.execute(sql)
        cols = [c[0] for c in cur.description]
        return _clean(pd.DataFrame(cur.fetchall(), columns=cols))
    finally:
        cur.close()