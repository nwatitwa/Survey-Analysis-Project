from pathlib import Path

import dash
from dash import dcc, html, Input, Output

from src.data.loader import load_data
from src.data.transforms import build_derived_tables
from src.data.filters import build_filter_options
from src.components.filter_panel import render_filter_panel
from src.pages import overview, demographics, remote_work, org_support


RAW_DF = load_data()
DERIVED = build_derived_tables(RAW_DF)
FILTER_OPTIONS = build_filter_options(DERIVED["base"])


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

app.layout = html.Div(
    className="app-shell",
    children=[
        html.Div(
            className="sidebar",
            children=[
                html.H2("Remote Work Survey"),
                html.P("Filter the results to explore patterns."),
                render_filter_panel(FILTER_OPTIONS),
            ],
        ),
        html.Div(
            className="content",
            children=[
                dcc.Tabs(
                    id="tabs",
                    value="overview",
                    className="tab-container",
                    children=[
                        dcc.Tab(label="Overview", value="overview", className="tab"),
                        dcc.Tab(
                            label="Demographics", value="demographics", className="tab"
                        ),
                        dcc.Tab(label="Remote Work", value="remote_work", className="tab"),
                        dcc.Tab(label="Org Support", value="org_support", className="tab"),
                    ],
                ),
                html.Div(id="tab-content"),
            ],
        ),
    ],
)


@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_tab(tab_value):
    if tab_value == "demographics":
        return demographics.layout()
    if tab_value == "remote_work":
        return remote_work.layout()
    if tab_value == "org_support":
        return org_support.layout()
    return overview.layout()


overview.register_callbacks(app, RAW_DF, DERIVED)
demographics.register_callbacks(app, RAW_DF, DERIVED)
remote_work.register_callbacks(app, RAW_DF, DERIVED)
org_support.register_callbacks(app, RAW_DF, DERIVED)


if __name__ == "__main__":
    app.run(debug=True)
