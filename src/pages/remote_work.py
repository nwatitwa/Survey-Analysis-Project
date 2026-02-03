from dash import html, dcc, Input, Output

from src.components.charts import gap_box, remote_pct_box
from src.components.filter_panel import FILTER_IDS
from src.components.kpi_cards import kpi_row
from src.data.filters import apply_filters


def layout() -> html.Div:
    return html.Div(
        className="page",
        children=[
            html.Div(id="remote-kpis"),
            dcc.Graph(id="remote-by-gender"),
            dcc.Graph(id="remote-by-orgsize"),
            dcc.Graph(id="remote-gaps"),
        ],
    )


def register_callbacks(app, raw_df, derived):
    base_df = derived["base"]
    remote_long = derived["remote_long"]
    gap_df = derived["gap_df"]

    @app.callback(
        Output("remote-kpis", "children"),
        Output("remote-by-gender", "figure"),
        Output("remote-by-orgsize", "figure"),
        Output("remote-gaps", "figure"),
        [
            Input(FILTER_IDS["gender"], "value"),
            Input(FILTER_IDS["age_group"], "value"),
            Input(FILTER_IDS["industry"], "value"),
            Input(FILTER_IDS["org_size"], "value"),
            Input(FILTER_IDS["location"], "value"),
        ],
    )
    def update_remote(gender, age_group, industry, org_size, location):
        filters = {
            "gender": gender,
            "age_group": age_group,
            "industry": industry,
            "org_size": org_size,
            "location": location,
        }
        filtered = apply_filters(base_df, filters)
        ids = set(filtered["response_id"].dropna().tolist())

        remote_filtered = (
            remote_long[remote_long["response_id"].isin(ids)]
            if remote_long is not None
            else remote_long
        )
        gaps_filtered = (
            gap_df[gap_df["response_id"].isin(ids)] if gap_df is not None else gap_df
        )

        gap_medians = (
            gaps_filtered.groupby("period_gap")["gap"].median()
            if gaps_filtered is not None and not gaps_filtered.empty
            else {}
        )
        kpis = kpi_row(
            [
                ("Median gap pre-COVID", f"{gap_medians.get('gap_precovid', 0):.1f}%"),
                ("Median gap last 3 months", f"{gap_medians.get('gap_covid', 0):.1f}%"),
                (
                    "Median gap future vs recent",
                    f"{gap_medians.get('gap_future_vs_recent', 0):.1f}%",
                ),
            ]
        )

        return (
            kpis,
            remote_pct_box(remote_filtered, "gender"),
            remote_pct_box(remote_filtered, "org_size"),
            gap_box(gaps_filtered),
        )

    return None
