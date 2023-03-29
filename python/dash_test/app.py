import sys
import logging
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

def layout():
    menu = dbc.Nav(
        [
            dbc.NavLink("Home", href=dash.page_registry['pages.home']['relative_path']),
            dbc.NavLink("Tasks", href=dash.page_registry['pages.tasks.index']['relative_path']),
        ]
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
                        align="left",
                        className="g-0",
                    ),
                    href="https://plotly.com",
                    className="navbar-brand",
                    style={"textDecoration": "none"},
                ),
                # dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    [
                        menu
                    ],
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                )
            ],
        ),
        color="dark",
        dark=True,
    )

    footer = html.Footer(
        [
            html.Div(
                [
                    html.P([ "© 2021 Copyright: JHU P&A" ])
                ],
                className="text-center p-4",
                style={ "background-color": "rgba(0, 0, 0, 0.05)" }
            )
        ],
        className="mt-auto"
    )
    
    return html.Div(
        [
            navbar,
            dbc.Container([
                dash.page_container
            ]),
            footer
        ],
        className="d-flex flex-column min-vh-100"
    )

class App():
    _default_index = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body class="d-flex flex-column min-vh-100">
        <!--[if IE]><script>
        alert("Dash v2.7+ does not support Internet Explorer. Please use a newer browser.");
        </script><![endif]-->
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""


    def __init__(self):
        self.app = None

    def start(self, debug=False):
        self.app = dash.Dash(
            __name__,
            use_pages=True,
            index_string=self._default_index,
            external_stylesheets=[ dbc.themes.BOOTSTRAP ])
        self.app.layout = layout()
        self.app.run_server(debug=debug)

if __name__ == "__main__":
    app = App()
    app.start(debug=(len(sys.argv) > 1 and sys.argv[1] == "debug"))
