import pandas as pd
import sqlite3
import requests
from pathlib import Path

default_folder = "data/"
def load_data_from_rule(rule: dict) -> pd.DataFrame:
    """
    Loads data depending on rule['data_source']['type'].
    
    Supports: CSV, Excel, SQLite, API
    """


    ds = rule.get("data_source", {})
    dtype = ds.get("type")

    if dtype == "csv":
        return _load_csv(ds, rule)

    elif dtype == "excel":
        return _load_excel(ds, rule)

    elif dtype == "sqlite":
        return _load_sqlite(ds, rule)

    elif dtype == "api":
        return _load_api(ds, rule)

    else:
        raise ValueError(f"Unsupported data_source type: {dtype}")


# ---------------------------
# CSV Loader
# ---------------------------
def _load_csv(ds, rule):
    global default_folder
    path = Path(default_folder + ds["path"])
    cols = rule.get("columns")

    df = pd.read_csv(path)
    return df[cols] if cols else df


# ---------------------------
# Excel Loader
# ---------------------------
def _load_excel(ds, rule):
    global default_folder
    path = Path(default_folder + ds["path"])
    cols = rule.get("columns")
    try:
        df = pd.read_excel(path)
        return df[cols] if cols else df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error


# ---------------------------
# SQLite Loader
# ---------------------------
def _load_sqlite(ds, rule):
    global default_folder
    db_path = Path(default_folder + ds["path"])
    table = ds["table"]
    cols = rule.get("columns")

    conn = sqlite3.connect(db_path)

    if cols:
        query = f"SELECT {', '.join(cols)} FROM {table}"
    else:
        query = f"SELECT * FROM {table}"

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# ---------------------------
# API Loader
# ---------------------------
def _load_api(ds, rule):
    url = ds["url"]
    cols = rule.get("columns")

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()  # assuming API returns JSON list
    df = pd.DataFrame(data)

    return df[cols] if cols else df


if __name__ == "__main__":
    sample_rule = {
        "data_source": {
            "type": "excel",
            "path": "metrics.xlsx"
        },
        "columns": ["debt_ratio", "liquidity_ratio", "daily_revenue"]
    }

    df = load_data_from_rule(sample_rule)
    print(df.head())

    sample_rule = {
        "data_source": {
            "type": "csv",
            "path": "metrics.csv"
        },
        "columns": ["debt_ratio", "liquidity_ratio", "daily_revenue"]
    }

    df = load_data_from_rule(sample_rule)
    print(df.head())


    sample_rule = {
        "data_source": {
            "type": "sqlite",
            "path": "finance.db",
            "table": "metrics",
        },
        "columns": ["date", "debt", "equity"]
    }

    df = load_data_from_rule(sample_rule)
    print(df.head())