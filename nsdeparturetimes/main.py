from datetime import datetime
import pytz
import os
from dash import Dash, html

from datacollection import ApiConnections, Departures
from generate_pages import generate_html_departure_display


external_stylesheets = []

app = Dash("nsdeparturestimes", external_stylesheets=external_stylesheets)
server = app.server

STATION_CODE = os.getenv("STATION_CODE")

connection = ApiConnections()

station_info = connection.get_station(station_code=STATION_CODE)

departures = Departures(station_code=STATION_CODE, station_name=station_info['namen']['middel'])

departures.parse_departures(connection.get_departures(departures.stationCode))
crowdness = connection.get_crowdedness(departures.departures.keys())
departures.update_departures(crowdness)
trains = connection.get_trains(departures.departures.keys())

tableformated = [data for _, data in departures.departures.items()]

current = datetime.now(tz=pytz.timezone("Europe/Amsterdam"))

departures.update_departures(trains)


header = html.Div(
    children=[
        html.Div(
            className="clock",
            children=[
                html.Img(src=app.get_asset_url("clock.svg"), className="clockimg"),
                current.strftime("%H:%M"),
                html.Div(children=[departures.stationName], className="station"),
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
        *generate_html_departure_display(departures.departures),
    ],
)

app.layout = html.Div(children=[header, new_table_layout])

if __name__ == "__main__":
    app.run_server(host="192.168.1.5", debug=True)
