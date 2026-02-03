import plotly.express as px
import plotly.graph_objects as go


EMPTY_FIG = go.Figure()


def empty_chart(title: str) -> go.Figure:
    fig = EMPTY_FIG.copy()
    fig.update_layout(title=title)
    return fig


def age_gender_bar(df):
    if df is None or df.empty:
        return empty_chart("Age by Gender")
    return px.bar(
        df,
        x="age_group",
        y="count",
        color="gender",
        barmode="stack",
        title="Age Distribution by Gender",
        labels={"age_group": "Age Group", "count": "Respondents", "gender": "Gender"},
    )


def industry_treemap(df):
    if df is None or df.empty:
        return empty_chart("Industry Breakdown")
    fig = px.treemap(
        df,
        path=["industry", "industry_detailed"],
        values="count",
        title="Industry Distribution",
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Respondents: %{value}<br>"
            "Share of sample: %{customdata[0]:.1f}%<extra></extra>"
        ),
        customdata=df[["percent"]].to_numpy(),
    )
    return fig


def orgsize_location_bar(df):
    if df is None or df.empty:
        return empty_chart("Org Size by Location")
    return px.bar(
        df,
        x="org_size",
        y="count",
        color="location",
        barmode="stack",
        title="Company Size by Location",
        labels={"org_size": "Company Size", "count": "Respondents", "location": "Location"},
    )


def remote_pct_box(df, x_field):
    if df is None or df.empty:
        return empty_chart("Remote Work %")
    return px.box(
        df,
        x=x_field,
        y="remote_pct",
        color="period",
        points="all",
        title=f"Remote Work % by {x_field.replace('_', ' ').title()}",
        labels={x_field: x_field.replace("_", " ").title(), "remote_pct": "Remote Work %"},
    )


def gap_box(df):
    if df is None or df.empty:
        return empty_chart("Preference Gaps")
    fig = px.box(
        df,
        x="period_gap",
        y="gap",
        points=False,
        title="Remote Work Preference Gaps",
        labels={"period_gap": "Gap Type", "gap": "Preferred - Actual (%)"},
    )
    fig.update_xaxes(
        categoryorder="array",
        categoryarray=["gap_precovid", "gap_covid", "gap_future_vs_recent"],
    )
    return fig


def org_support_trends(df):
    if df is None or df.empty:
        return empty_chart("Org Support Over Time")
    fig = px.line(
        df,
        x="period",
        y="score",
        color="question",
        markers=True,
        title="Organization Support Over Time",
        labels={"score": "Average score (1-5)"},
    )
    fig.update_xaxes(
        categoryorder="array",
        categoryarray=["Last Year", "Last 3 Months", "Future"],
    )
    return fig


def time_allocation_bar(df):
    if df is None or df.empty:
        return empty_chart("Time Allocation")
    return px.bar(
        df,
        x="activity",
        y="hours",
        color="work_type",
        barmode="group",
        title="Average Hours per Activity",
        labels={"activity": "Activity", "hours": "Hours"},
    )
