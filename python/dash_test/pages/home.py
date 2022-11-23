import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, path='/')

def layout(**kwargs):
    html.Div([
        html.H1('This is our Home page'),
        html.Div([
            "Select a city: ",
        ]),
        html.Br(),
        html.Div(id='analytics-output'),
])
