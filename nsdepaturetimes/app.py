from datetime import datetime
import pytz
from dash import Dash, html

from datacollection import ApiConnections, Departures


external_stylesheets = []

app = Dash("nsdeparturestimes", external_stylesheets=external_stylesheets)
server = app.server

connection = ApiConnections()
departures = Departures()

departures.parse_departures(connection.get_departures("BD"))
crowdness = connection.get_crowdedness(departures.departures.keys())
departures.update_departures(crowdness)
trains = connection.get_trains(departures.departures.keys())

tableformated = [data for _, data in departures.departures.items()]

current = datetime.now(tz=pytz.timezone("Europe/Amsterdam"))

departures.update_departures(trains)

layout = []
for train, data in departures.departures.items():
    headers = [
        html.H2(
            f"{data['name']} vertrek in {data['timeBeforeLeave']} minuten"
            + (
                f", waarvan {data['delay']} minuten vertraging"
                if data["delay"] > 0
                else ""
            )
        ),
        html.P(
            f"Vertrekt om: {data['actualDateTime'].strftime('%H:%M')} van spoor: {data['track']}"
        ),
    ]
    items = [
        html.P(
            f"{data['trainCategory']} met treinnummer: {train} naar {data['direction']}"
        ),
        html.Img(src=app.get_asset_url(f'{data["classifiction"]}.svg')),
    ]
    total_width = 0
    for materieel in data["materieel"]:
        total_width += materieel["breedte"]
    images = [
        html.Img(
            src=i["afbeelding"],
            style={"width": f"{i['breedte']/total_width*100}%"},
        )
        for i in data["materieel"]
        if "afbeelding" in i.keys()
    ]
    layout += [
        html.Div(
            children=[*headers, *images, *items],
            id=train,
            style={"opacity": 0.1 if data["cancelled"] else 1},
        ),
        html.Hr(),
    ]


new_layout = []

for train, data in departures.departures.items():
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
                                    children=data["actualDateTime"].strftime("%H:%M"),
                                )
                            ],
                        )
                    ],
                ),
                html.Div(
                    className="column destination",
                    children=[
                        html.Div(
                            className="destination",
                            children=html.Div(
                                className="actual-destination",
                                children=data["direction"],
                            ),
                        ),
                        html.Div(className="via", children="via"),
                    ],
                ),
                html.Div(
                    className="column platform",
                    children=[
                        html.Div(className="platform-indicator", children=data["track"])
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
                                        src=app.get_asset_url(
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
                                            "max-width": f"{i['breedte']/total_width*100}%",
                                            "max-height": "100%",
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


header = html.Div(
    children=[
        html.Div(
            className="clock",
            children=[
                html.Img(src=app.get_asset_url("clock.svg"), className="clockimg"),
                current.strftime("%H:%M"),
                html.Div(children=["Breda"], className="station"),
            ],
        )
    ],
    id="departures-header",
    className="style-tb",
)

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
        *new_layout,
    ],
)

app.layout = html.Div(children=[header, new_table_layout, *layout])

if __name__ == "__main__":
    app.run_server(host="192.168.1.5", debug=True)
