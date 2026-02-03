from dash import html


def kpi_row(kpis: list[tuple[str, str]]) -> html.Div:
    cards = []
    for label, value in kpis:
        cards.append(
            html.Div(
                className="kpi-card",
                children=[
                    html.Div(label, className="kpi-label"),
                    html.Div(value, className="kpi-value"),
                ],
            )
        )
    return html.Div(cards, className="kpi-row")
