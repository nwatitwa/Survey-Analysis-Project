import pandas as pd


FILTER_FIELDS = {
    "gender": "gender",
    "age_group": "age_group",
    "industry": "industry",
    "org_size": "org_size",
    "location": "location",
}


def build_filter_options(df: pd.DataFrame) -> dict:
    options = {}
    for key, col in FILTER_FIELDS.items():
        if col not in df.columns:
            options[key] = []
            continue
        values = (
            df[col]
            .dropna()
            .astype(str)
            .sort_values()
            .unique()
            .tolist()
        )
        options[key] = values
    return options


def _coerce_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    filtered = df
    for key, col in FILTER_FIELDS.items():
        values = _coerce_list(filters.get(key))
        if values and col in filtered.columns:
            filtered = filtered[filtered[col].isin(values)]
    return filtered
