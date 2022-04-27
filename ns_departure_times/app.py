from dash import Dash

external_stylesheets = []
app = Dash("ns-departure-times", external_stylesheets=external_stylesheets)
server = app.server