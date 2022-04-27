from dash import Dash

external_stylesheets = []
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server