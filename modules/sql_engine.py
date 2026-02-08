import sqlite3
import pandas as pd

def query_sql(df, sql):
    conn = sqlite3.connect(":memory:")
    df.to_sql("data", conn, index=False, if_exists="replace")

    try:
        return pd.read_sql(sql, conn)
    except Exception as e:
        return str(e)
