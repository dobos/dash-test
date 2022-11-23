import sys
import logging
import dash

from .layout import layout

class App():
    def __init__(self):
        self.app = None
        self.server = None

    def start(self, debug=False):
        self.app = dash.Dash(__name__, use_pages=True)
        self.app.layout = layout()
        self.app.run_server(debug=debug)

if __name__ == "__main__":
    app = App()
    app.start(debug=(len(sys.argv) > 1 and sys.argv[1] == "debug"))
