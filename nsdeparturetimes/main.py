from datetime import datetime

import pytz
from dash import Input, Output, State, dcc, html, ALL, callback_context

from app import app, server
from generate_pages import departures, generate_layout


app.layout = html.Div(
    children=[
        dcc.Interval(id="data_refresh", interval=30000, n_intervals=0),
        dcc.Interval(id="style_updates", interval=5000, n_intervals=0),
        html.Div(
            children=[
                html.Div(
                    className="clock",
                    children=[
                        html.Img(
                            src=app.get_asset_url("clock.svg"), className="clockimg"
                        ),
                        html.Div(
                            datetime.now(tz=pytz.timezone("Europe/Amsterdam")).strftime(
                                "%H:%M"
                            ),
                            id="clocktime",
                            className="clock",
                        ),
                        html.Div(
                            children=[departures.stationName], className="station"
                        ),
                    ],
                )
            ],
            id="departures-header",
            className="style-tb",
        ),
        html.Div(id="page_contents", children=generate_layout()),
    ]
)


@app.callback(
    Output("page_contents", "children"),
    Output("clocktime", "children"),
    Input("data_refresh", "n_intervals"),
)
def update_layout(n_intervals: int) -> list:
    return generate_layout(), datetime.now(
        tz=pytz.timezone("Europe/Amsterdam")
    ).strftime("%H:%M")


@app.callback(
    Output({"category": "via", "trainNumber": ALL, "type": "switching"}, "hidden"),
    Output({"category": "remark", "trainNumber": ALL, "type": "switching"}, "hidden"),
    Input("style_updates", "n_intervals"),
)
def switch_style(n_intervals):
    given_outputs = callback_context.outputs_list
    if len(given_outputs[0]) == len(given_outputs[1]):
        if n_intervals % 2 == 0:
            return len(given_outputs[0]) * [False], len(given_outputs[1]) * [True]
        else:
            return len(given_outputs[0]) * [True], len(given_outputs[1]) * [False]


if __name__ == "__main__":
    app.run_server(host="192.168.1.5", debug=True)
