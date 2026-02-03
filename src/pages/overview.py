from dash import html, dcc, Input, Output

from src.components.charts import (
    age_gender_bar,
    industry_treemap,
    orgsize_location_bar,
)
from src.components.kpi_cards import kpi_row
from src.components.filter_panel import FILTER_IDS
from src.data.filters import apply_filters


def layout() -> html.Div:
    return html.Div(
        className="page",
        children=[
            html.Div(id="overview-kpis"),
            dcc.Graph(id="overview-age-gender"),
            dcc.Graph(id="overview-industry-tree"),
            dcc.Graph(id="overview-orgsize-location"),
        ],
    )


def register_callbacks(app, raw_df, derived):
    base_df = derived["base"]

    @app.callback(
        Output("overview-kpis", "children"),
        Output("overview-age-gender", "figure"),
        Output("overview-industry-tree", "figure"),
        Output("overview-orgsize-location", "figure"),
        [
            Input(FILTER_IDS["gender"], "value"),
            Input(FILTER_IDS["age_group"], "value"),
            Input(FILTER_IDS["industry"], "value"),
            Input(FILTER_IDS["org_size"], "value"),
            Input(FILTER_IDS["location"], "value"),
        ],
    )
    def update_overview(gender, age_group, industry, org_size, location):
        filters = {
            "gender": gender,
            "age_group": age_group,
            "industry": industry,
            "org_size": org_size,
            "location": location,
        }
        filtered = apply_filters(base_df, filters)

        total = f"{len(filtered):,}"
        avg_last_year = (
            filtered["remote_work_pct_last_year"].mean()
            if "remote_work_pct_last_year" in filtered.columns
            else 0
        )
        avg_last_3m = (
            filtered["remote_work_pct_last_3_months"].mean()
            if "remote_work_pct_last_3_months" in filtered.columns
            else 0
        )
        avg_future = (
            filtered["remote_work_pref_pct_future"].mean()
            if "remote_work_pref_pct_future" in filtered.columns
            else 0
        )

        kpis = kpi_row(
            [
                ("Respondents", total),
                ("Avg remote % last year", f"{avg_last_year:.1f}%"),
                ("Avg remote % last 3 months", f"{avg_last_3m:.1f}%"),
                ("Avg preferred remote % future", f"{avg_future:.1f}%"),
            ]
        )

        age_gender = (
            filtered[["age_group", "gender"]]
            .dropna()
            .groupby(["age_group", "gender"])
            .size()
            .reset_index(name="count")
        )
        industry_counts = (
            filtered[["industry", "industry_detailed"]]
            .dropna()
            .groupby(["industry", "industry_detailed"])
            .size()
            .reset_index(name="count")
        )
        if not industry_counts.empty:
            industry_counts["percent"] = (
                industry_counts["count"] / industry_counts["count"].sum() * 100
            )

        org_loc = (
            filtered[["org_size", "location"]]
            .dropna()
            .groupby(["org_size", "location"])
            .size()
            .reset_index(name="count")
        )

        return (
            kpis,
            age_gender_bar(age_gender),
            industry_treemap(industry_counts),
            orgsize_location_bar(org_loc),
        )

    return None
