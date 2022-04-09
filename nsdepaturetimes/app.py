from dash import Dash, html, dash_table

import json

from datacollection import ApiConnections, Depatures


external_stylesheets = []

app = Dash("nsdepaturetimes", external_stylesheets=external_stylesheets)
server = app.server

connection = ApiConnections()
depature = Depatures()

depature.parse_depatures(connection.get_depatures("BD"))
crowdness = connection.get_crowdedness(depature.depatures.keys())
depature.update_depatures(crowdness)
trains = connection.get_trains(depature.depatures.keys())

tableformated = [data for _, data in depature.depatures.items()]

depature.update_depatures(trains)

layout = []
for train, data in depature.depatures.items():
    headers = [
        html.H2(
            f"{data['name']} vertrek in {data['timeBeforeLeave']} minuten"
            + (
                f", waarvan {data['delay']} minuten vertraging"
                if data["delay"] > 0
                else ""
            )
        ),
        html.P(f"Vertrekt om: {data['actualDateTime'].strftime('%H:%M')} van spoor: {data['track']}"),
    ]
    items = [
        html.P(
            f"{data['trainCategory']} met treinnummer: {train} naar {data['direction']}"
        ),
        html.Img(src=app.get_asset_url(f'{data["classifiction"]}.svg')),
    ]
    aantal_bakken = 0
    for materieel in data["materieel"]:
        aantal_bakken += len(materieel["bakken"]) + 1
    images = [
        html.Img(
            src=i["afbeelding"],
            style={"width": f"{(len(i['bakken']) + 1)/aantal_bakken*100}%"},
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

app.layout = html.Div(
    [html.H1("Hello Dash"), dash_table.DataTable(data=tableformated), *layout],
)

if __name__ == "__main__":
    app.run_server(debug=True)
