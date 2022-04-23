from dash import html
from nsdeparturetimes import main


def generate_html_departure_display(departures: dict) -> list:
    new_layout = []
    for train, data in departures.items():
        total_width = 0
        for materieel in data["materieel"]:
            total_width += materieel["breedte"]
        if data["cancelled"]:
            row_class = "row cancelled"
        else:
            row_class = "row"
        new_layout += [
            html.Div(
                className=row_class,
                children=[
                    html.Div(
                        className="column time",
                        children=[
                            html.Div(
                                className="departures-time departure_time",
                                children=[
                                    html.Div(
                                        className="departure_time",
                                        children=data["actualDateTime"].strftime(
                                            "%H:%M"
                                        ),
                                    )
                                ],
                            )
                        ],
                    ),
                    html.Div(
                        className="column destination",
                        children=[
                            html.Div(
                                className="destinations",
                                children=html.Div(
                                    className="actual-destination",
                                    children=data["direction"],
                                ),
                            ),
                            html.Div(
                                className="via",
                                children=f"via {','.join(data['via'])}"
                                if len(data["via"]) > 0
                                else "",
                            ),
                            html.Div(className="remarks", children=data["messages"]),
                        ],
                    ),
                    html.Div(
                        className="column platform",
                        children=[
                            html.Div(
                                className="platform-indicator platform-changed"
                                if data["changedPlatform"]
                                else "platform-indicator",
                                children=data["track"],
                            )
                        ],
                    ),
                    html.Div(
                        className="column train",
                        children=[
                            html.Div(
                                className="train-id",
                                children=[
                                    train,
                                    html.Div(
                                        className="crowdedness",
                                        children=html.Img(
                                            src=main.app.get_asset_url(
                                                f'{data["classifiction"]}.svg'
                                            )
                                        ),
                                    ),
                                ],
                            )
                        ],
                    ),
                    html.Div(
                        className="column material",
                        children=[
                            html.Span(
                                [
                                    html.Span(
                                        html.Img(
                                            src=i["afbeelding"],
                                            style={
                                                "maxWidth": f"{i['breedte']/total_width*100}%",
                                                "maxHeight": "100%",
                                            },
                                        )
                                    )
                                    for i in data["materieel"]
                                    if "afbeelding" in i.keys()
                                ]
                            ),
                        ],
                    ),
                ],
            )
        ]

    return new_layout