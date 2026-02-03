from __future__ import annotations

import pandas as pd


SURVEY_YEAR = 2020

AGE_BINS = [18, 25, 35, 45, 55, 65, 100]
AGE_LABELS = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]

PERIOD_MAP = {
    "remote_work_pct_last_year": "Pre-COVID",
    "remote_work_pct_last_3_months": "During-COVID",
    "remote_work_pref_pct_future": "Future Preference",
}

PERIOD_ORDER = ["Pre-COVID", "During-COVID", "Future Preference"]

SUPPORT_MAP = {
    "remote_last_year_org_encouraged_agreement": ("Last Year", "Encouraged"),
    "remote_last_year_org_prepared_agreement": ("Last Year", "Prepared"),
    "remote_last_year_common_practice_agreement": ("Last Year", "Common practice"),
    "remote_last_year_permission_easy_agreement": ("Last Year", "Permission easy"),
    "remote_last_year_collaboration_easy_agreement": ("Last Year", "Collaboration"),
    "remote_last_year_recommend_agreement": ("Last Year", "Recommend"),
    "remote_last_3_months_org_encouraged_agreement": ("Last 3 Months", "Encouraged"),
    "remote_last_3_months_org_prepared_agreement": ("Last 3 Months", "Prepared"),
    "remote_last_3_months_common_practice_agreement": ("Last 3 Months", "Common practice"),
    "remote_last_3_months_permission_easy_agreement": ("Last 3 Months", "Permission easy"),
    "remote_last_3_months_collaboration_easy_agreement": ("Last 3 Months", "Collaboration"),
    "remote_last_3_months_recommend_agreement": ("Last 3 Months", "Recommend"),
    "Imagine that COVID-19 is cured or eradicated. How likely would you consider the following statements? - My employer would encourage more remote working": (
        "Future",
        "Encouraged",
    ),
    "Imagine that COVID-19 is cured or eradicated. How likely would you consider the following statements? - My employer would make changes to support remote working": (
        "Future",
        "Prepared",
    ),
    "Imagine that COVID-19 is cured or eradicated. How likely would you consider the following statements? - I would have more choice about whether I work remotely": (
        "Future",
        "Choice",
    ),
}

TIME_COLUMNS = {
    "onsite_commute_hours": ("Onsite", "Commute"),
    "onsite_work_hours": ("Onsite", "Work"),
    "onsite_personal_hours": ("Onsite", "Personal"),
    "onsite_caring_hours": ("Onsite", "Caring"),
    "remote_commute_hours": ("Remote", "Commute"),
    "remote_work_hours": ("Remote", "Work"),
    "remote_personal_hours": ("Remote", "Personal"),
    "remote_caring_hours": ("Remote", "Caring"),
}


def build_derived_tables(df: pd.DataFrame) -> dict:
    base = df.copy()
    if "response_id" not in base.columns:
        base["response_id"] = base.index.astype(str)

    if "birth_year" in base.columns:
        base["age"] = SURVEY_YEAR - pd.to_numeric(base["birth_year"], errors="coerce")
        base["age_group"] = pd.cut(
            base["age"],
            bins=AGE_BINS,
            labels=AGE_LABELS,
            right=False,
        )

    remote_cols = [c for c in PERIOD_MAP if c in base.columns]
    remote_long = None
    if remote_cols:
        remote_long = (
            base[
                [
                    "response_id",
                    "age_group",
                    "gender",
                    "org_size",
                    "industry",
                ]
                + remote_cols
            ]
            .dropna(subset=remote_cols)
            .melt(
                id_vars=["response_id", "age_group", "gender", "org_size", "industry"],
                value_vars=remote_cols,
                var_name="period",
                value_name="remote_pct",
            )
        )
        remote_long["period"] = remote_long["period"].map(PERIOD_MAP)

    gap_df = None
    if all(
        col in base.columns
        for col in [
            "remote_work_pct_last_year",
            "remote_work_pref_pct_last_year",
            "remote_work_pct_last_3_months",
            "remote_work_pref_pct_last_3_months",
            "remote_work_pref_pct_future",
        ]
    ):
        gap_base = base[
            [
                "response_id",
                "remote_work_pct_last_year",
                "remote_work_pref_pct_last_year",
                "remote_work_pct_last_3_months",
                "remote_work_pref_pct_last_3_months",
                "remote_work_pref_pct_future",
            ]
        ].dropna()
        gap_base["gap_precovid"] = (
            gap_base["remote_work_pref_pct_last_year"]
            - gap_base["remote_work_pct_last_year"]
        )
        gap_base["gap_covid"] = (
            gap_base["remote_work_pref_pct_last_3_months"]
            - gap_base["remote_work_pct_last_3_months"]
        )
        gap_base["gap_future_vs_recent"] = (
            gap_base["remote_work_pref_pct_future"]
            - gap_base["remote_work_pct_last_3_months"]
        )
        gap_df = gap_base.melt(
            id_vars=["response_id"],
            value_vars=["gap_precovid", "gap_covid", "gap_future_vs_recent"],
            var_name="period_gap",
            value_name="gap",
        )

    support_frames = []
    for col, (period, question) in SUPPORT_MAP.items():
        if col in base.columns:
            frame = base[["response_id", col]].dropna().rename(columns={col: "score"})
            frame["period"] = period
            frame["question"] = question
            support_frames.append(frame)
    org_support_long = (
        pd.concat(support_frames, ignore_index=True) if support_frames else None
    )

    time_frames = []
    for col, (work_type, activity) in TIME_COLUMNS.items():
        if col in base.columns:
            frame = base[["response_id", col]].dropna().rename(columns={col: "hours"})
            frame["work_type"] = work_type
            frame["activity"] = activity
            time_frames.append(frame)
    time_long = pd.concat(time_frames, ignore_index=True) if time_frames else None

    return {
        "base": base,
        "remote_long": remote_long,
        "gap_df": gap_df,
        "org_support_long": org_support_long,
        "time_long": time_long,
    }
