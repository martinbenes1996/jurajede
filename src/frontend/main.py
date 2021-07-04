
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from . import nav
# pages
from . import page_home
from . import page_yearly
from . import page_series
from . import page_data

def layout():
    sidebar = nav.layout()
    content = html.Div(id="page-content")
    return html.Div([dcc.Location(id="url"), sidebar, content], style={'height': '90vh'})

def register(app):
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/":
            return page_home.layout()
        elif pathname == "/total":
            return page_series.layout()
        elif pathname == "/yearly":
            return page_yearly.layout()
        elif pathname == "/data":
            return page_data.layout()
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron([
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised...")
        ])
    @app.callback(
        Output("sidebar", "className"),
        [Input("sidebar-toggle", "n_clicks")],
        [State("sidebar", "className")],
    )
    def toggle_classname(n, classname):
        if n and classname == "":
            return "collapsed"
        return ""
    @app.callback(
        Output("collapse", "is_open"),
        [Input("navbar-toggle", "n_clicks")],
        [State("collapse", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open