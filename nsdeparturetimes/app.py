from dash import Dash

external_stylesheets = []
app = Dash("nsdeparturestimes", external_stylesheets=external_stylesheets)
server = app.server