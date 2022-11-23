import sys
import logging
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

def layout():
    # menu = html.Div([
    #     dcc.Link("home", href=dash.page_registry['pages.home']['relative_path']),
    #     dcc.Link("tasks", href=dash.page_registry['pages.tasks.index']['relative_path']),
    # ])

    menu = dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem("Home", href=dash.page_registry['pages.home']['relative_path']),
            dbc.DropdownMenuItem("Task", href=dash.page_registry['pages.tasks.index']['relative_path']),
        ],
        nav=True,
        in_navbar=True,
        label="More",
    )

    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="", height="30px")),
                            dbc.Col(dbc.NavbarBrand("Example Dashboard", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="https://plotly.com",
                    style={"textDecoration": "none"},
                ),
                menu,
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)
            ]
        ),
        color="dark",
        dark=True,
    )
    
    # navbar = dbc.Navbar([
    #         html.H1("Example dashboard"),
    #         menu
    #     ],
    #     style={
    #         'backgroundColor': 'yellow',
    #         'color': 'black'
    #     }
    # )

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

class App():
    def __init__(self):
        self.app = None
        self.server = None

    def start(self, debug=False):
        self.app = dash.Dash(
            __name__,
            use_pages=True,
            external_stylesheets=[ dbc.themes.BOOTSTRAP ])
        self.app.layout = layout()
        self.app.run_server(debug=debug)

if __name__ == "__main__":
    app = App()
    app.start(debug=(len(sys.argv) > 1 and sys.argv[1] == "debug"))
