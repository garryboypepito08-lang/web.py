import json
from pathlib import Path
from datetime import datetime
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(filename, payload):
    path = DATA_DIR / filename
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def current_time_manila():
    now = datetime.now()
    return now.strftime("%I:%M %p")


def format_currency(value):
    return f"PHP {float(value):,.2f}"


def to_df(records):
    return pd.DataFrame(records)
