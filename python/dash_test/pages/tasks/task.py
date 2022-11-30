import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__)

def layout(task_id=None, **kwargs):
    return html.Div([
        html.H1(f'This is our Task No. {task_id} page'),
        html.Div([
            "Select a city: ",
        ]),
        html.Br(),
        html.Div(id='analytics-output'),
    ])
