import dash
from dash import html, dcc, callback, Input, Output

def layout():
    menu = html.Div([
        dcc.Link("home", href=dash.page_registry['pages.home']['relative_path']),
        dcc.Link("tasks", href=dash.page_registry['pages.tasks.index']['relative_path']),
    ])
    
    navbar = html.Div([
            html.H1("Example dashboard"),
            menu
        ],
        style={
            'backgroundColor': 'yellow',
            'color': 'black'
        }
    )

    return html.Div(
        [
            navbar,
            html.Br(),
            html.Div([
                    html.H2(["contents come here:"]),
                    dash.page_container
                ]
            ),
            html.Br(),
            html.Div()],
        )