from functools import lru_cache
from pathlib import Path

import pandas as pd


DEFAULT_DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "Datasets"
    / "Cleaned Data"
    / "cleaned_2020.csv"
)


@lru_cache(maxsize=2)
def load_data(path: Path | None = None) -> pd.DataFrame:
    data_path = Path(path) if path else DEFAULT_DATA_PATH
    return pd.read_csv(data_path, encoding="latin1")
