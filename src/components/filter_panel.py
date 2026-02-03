from dash import html, dcc


FILTER_IDS = {
    "gender": "filter-gender",
    "age_group": "filter-age-group",
    "industry": "filter-industry",
    "org_size": "filter-org-size",
    "location": "filter-location",
}


def render_filter_panel(options: dict) -> html.Div:
    return html.Div(
        className="filter-panel",
        children=[
            html.Div(
                className="filter-group",
                children=[
                    html.Label("Gender"),
                    dcc.Dropdown(
                        id=FILTER_IDS["gender"],
                        options=[
                            {"label": v, "value": v}
                            for v in options.get("gender", [])
                        ],
                        multi=True,
                        placeholder="All",
                    ),
                ],
            ),
            html.Div(
                className="filter-group",
                children=[
                    html.Label("Age Group"),
                    dcc.Dropdown(
                        id=FILTER_IDS["age_group"],
                        options=[
                            {"label": v, "value": v}
                            for v in options.get("age_group", [])
                        ],
                        multi=True,
                        placeholder="All",
                    ),
                ],
            ),
            html.Div(
                className="filter-group",
                children=[
                    html.Label("Industry"),
                    dcc.Dropdown(
                        id=FILTER_IDS["industry"],
                        options=[
                            {"label": v, "value": v}
                            for v in options.get("industry", [])
                        ],
                        multi=True,
                        placeholder="All",
                    ),
                ],
            ),
            html.Div(
                className="filter-group",
                children=[
                    html.Label("Org Size"),
                    dcc.Dropdown(
                        id=FILTER_IDS["org_size"],
                        options=[
                            {"label": v, "value": v}
                            for v in options.get("org_size", [])
                        ],
                        multi=True,
                        placeholder="All",
                    ),
                ],
            ),
            html.Div(
                className="filter-group",
                children=[
                    html.Label("Location"),
                    dcc.Dropdown(
                        id=FILTER_IDS["location"],
                        options=[
                            {"label": v, "value": v}
                            for v in options.get("location", [])
                        ],
                        multi=True,
                        placeholder="All",
                    ),
                ],
            ),
        ],
    )
