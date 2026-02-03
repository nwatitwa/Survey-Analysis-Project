from dash import html, dcc, Input, Output

from src.components.charts import org_support_trends, time_allocation_bar
from src.components.filter_panel import FILTER_IDS
from src.components.kpi_cards import kpi_row
from src.data.filters import apply_filters


def layout() -> html.Div:
    return html.Div(
        className="page",
        children=[
            html.Div(id="support-kpis"),
            dcc.Graph(id="support-trends"),
            dcc.Graph(id="time-allocation"),
        ],
    )


def register_callbacks(app, raw_df, derived):
    base_df = derived["base"]
    support_long = derived["org_support_long"]
    time_long = derived["time_long"]

    @app.callback(
        Output("support-kpis", "children"),
        Output("support-trends", "figure"),
        Output("time-allocation", "figure"),
        [
            Input(FILTER_IDS["gender"], "value"),
            Input(FILTER_IDS["age_group"], "value"),
            Input(FILTER_IDS["industry"], "value"),
            Input(FILTER_IDS["org_size"], "value"),
            Input(FILTER_IDS["location"], "value"),
        ],
    )
    def update_support(gender, age_group, industry, org_size, location):
        filters = {
            "gender": gender,
            "age_group": age_group,
            "industry": industry,
            "org_size": org_size,
            "location": location,
        }
        filtered = apply_filters(base_df, filters)
        ids = set(filtered["response_id"].dropna().tolist())

        support_filtered = (
            support_long[support_long["response_id"].isin(ids)]
            if support_long is not None
            else support_long
        )
        time_filtered = (
            time_long[time_long["response_id"].isin(ids)]
            if time_long is not None
            else time_long
        )

        support_summary = (
            support_filtered.groupby(["period", "question"], as_index=False)["score"]
            .mean()
            if support_filtered is not None and not support_filtered.empty
            else support_filtered
        )
        time_summary = (
            time_filtered.groupby(["work_type", "activity"], as_index=False)["hours"]
            .mean()
            if time_filtered is not None and not time_filtered.empty
            else time_filtered
        )

        support_last_year = (
            support_summary[support_summary["period"] == "Last Year"]["score"].mean()
            if support_summary is not None and not support_summary.empty
            else 0
        )
        support_last_3m = (
            support_summary[support_summary["period"] == "Last 3 Months"]["score"].mean()
            if support_summary is not None and not support_summary.empty
            else 0
        )
        commute_gap = 0
        if time_summary is not None and not time_summary.empty:
            onsite = time_summary[
                (time_summary["work_type"] == "Onsite")
                & (time_summary["activity"] == "Commute")
            ]["hours"].mean()
            remote = time_summary[
                (time_summary["work_type"] == "Remote")
                & (time_summary["activity"] == "Commute")
            ]["hours"].mean()
            commute_gap = onsite - remote

        kpis = kpi_row(
            [
                ("Avg support last year", f"{support_last_year:.2f}"),
                ("Avg support last 3 months", f"{support_last_3m:.2f}"),
                ("Commute hours saved", f"{commute_gap:.2f}"),
            ]
        )

        return (
            kpis,
            org_support_trends(support_summary),
            time_allocation_bar(time_summary),
        )

    return None
