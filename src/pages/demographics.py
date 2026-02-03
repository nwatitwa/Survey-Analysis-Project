from dash import html, dcc, Input, Output

from src.components.charts import (
    age_gender_bar,
    industry_treemap,
    orgsize_location_bar,
)
from src.components.filter_panel import FILTER_IDS
from src.components.kpi_cards import kpi_row
from src.data.filters import apply_filters


def layout() -> html.Div:
    return html.Div(
        className="page",
        children=[
            html.Div(id="demographics-kpis"),
            dcc.Graph(id="demographics-age-gender"),
            dcc.Graph(id="demographics-industry-tree"),
            dcc.Graph(id="demographics-orgsize-location"),
        ],
    )


def register_callbacks(app, raw_df, derived):
    base_df = derived["base"]

    @app.callback(
        Output("demographics-kpis", "children"),
        Output("demographics-age-gender", "figure"),
        Output("demographics-industry-tree", "figure"),
        Output("demographics-orgsize-location", "figure"),
        [
            Input(FILTER_IDS["gender"], "value"),
            Input(FILTER_IDS["age_group"], "value"),
            Input(FILTER_IDS["industry"], "value"),
            Input(FILTER_IDS["org_size"], "value"),
            Input(FILTER_IDS["location"], "value"),
        ],
    )
    def update_demographics(gender, age_group, industry, org_size, location):
        filters = {
            "gender": gender,
            "age_group": age_group,
            "industry": industry,
            "org_size": org_size,
            "location": location,
        }
        filtered = apply_filters(base_df, filters)

        total = f"{len(filtered):,}"
        median_age = (
            filtered["age"].median() if "age" in filtered.columns else 0
        )
        top_industry = ""
        if "industry" in filtered.columns:
            top_industry = (
                filtered["industry"].value_counts().index[0]
                if not filtered["industry"].dropna().empty
                else ""
            )

        kpis = kpi_row(
            [
                ("Respondents", total),
                ("Median age", f"{median_age:.0f}"),
                ("Top industry", top_industry or "N/A"),
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
