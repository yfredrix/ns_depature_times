import os
from dash import html, dcc, Input, Output, State

from app import app, server

from generate_pages import generate_layout


STATION_CODE = os.getenv("STATION_CODE")

app.layout = html.Div(
    children=[
        dcc.Interval(id="data_refresh", interval=30000, n_intervals=0),
        html.Div(id="page_contents", children=generate_layout()),
    ]
)

@app.callback(
    Output("page_contents", "children"),
    Input("data_refresh", "n_intervals"),
)
def update_layout(n_intervals: int) -> list:
    return generate_layout()

if __name__ == "__main__":
    app.run_server(host="192.168.1.5", debug=True)
