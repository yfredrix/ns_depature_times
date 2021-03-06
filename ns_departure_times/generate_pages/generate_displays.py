import os

from dash import html
from ns_departure_times.datacollection import ApiConnections, Departures
from ns_departure_times.app import app

STATION_CODE = os.getenv("STATION_CODE")
MINIMUM_DEPATURE_TIME = int(os.getenv("MINIMUM_DEPARTURE_TIME", "0"))
connection = ApiConnections()

station_info = connection.get_station(station_code=STATION_CODE)
departures = Departures(
    station_code=STATION_CODE, station_name=station_info["namen"]["middel"]
)


def generate_layout() -> list:
    """Generate the entire layout with new data from the current departure times"""
    departures.parse_departures(connection.get_departures(departures.stationCode))
    crowdness = connection.get_crowdedness(departures.departures.keys())
    departures.update_departures(crowdness)
    trains = connection.get_trains(departures.departures.keys())
    departures.update_departures(trains)

    new_table_layout = html.Div(
        id="departures-main",
        className="style-tb",
        children=[
            html.Div(
                children=[
                    html.Div(className="column time", children="Vertrek"),
                    html.Div(
                        className="column destination",
                        children="Bestemming / Opmerkingen",
                    ),
                    html.Div(className="column platform", children="Spoor"),
                    html.Div(className="column train", children="Trein"),
                ],
                id="departures-header-row",
            ),
            *generate_html_departure_display(departures.departures),
        ],
    )
    return new_table_layout


def generate_html_departure_display(departures: dict) -> list:
    new_layout = []
    for train, data in departures.items():
        if data["timeBeforeLeave"] >= MINIMUM_DEPATURE_TIME:
            if (
                len(data["materieel"]) > 0
                and "afbeelding" in data["materieel"][0].keys()
            ):
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
                                    id={
                                        "trainNumber": train,
                                        "type": "switching",
                                        "category": "via",
                                    }
                                    if data["messages"]
                                    else {
                                        "trainNumber": train,
                                        "type": "normal",
                                        "category": "via",
                                    },
                                    className="via",
                                    children=f"via {', '.join(data['via'])}"
                                    if len(data["via"]) > 0
                                    else "",
                                ),
                                html.Div(
                                    id={
                                        "trainNumber": train,
                                        "type": "switching",
                                        "category": "remark",
                                    },
                                    className="remarks",
                                    children=data["messages"],
                                )
                                if data["messages"]
                                else "",
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
                                        f"{data['trainCategory']} {train}",
                                        html.Div(
                                            className="crowdedness",
                                            children=html.Img(
                                                src=app.get_asset_url(
                                                    f'{data["classifiction"]}.svg'
                                                )
                                            ),
                                        )
                                        if "classifiction" in data.keys()
                                        else "",
                                        html.Div(
                                            className="delay",
                                            children=f"+ {data['delay']} min",
                                        )
                                        if data["delay"] > 0
                                        else "",
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
                        )
                        if len(data["materieel"]) > 0
                        and "afbeelding" in data["materieel"][0].keys()
                        else "",
                    ],
                )
            ]

    return new_layout
