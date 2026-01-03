import pandas as pd
from pathlib import Path

def load_metrics():
    path = Path("data/metrics.csv")
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.sort_values("date")
    return df
