
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from . import config
from . import nav
# pages
from . import page_home
#from . import page_yearly
from . import page_total
from . import page_about
from . import page_data

def layout():
    #print("main.layout()")
    sidebar = nav.layout()
    content = html.Div([
        html.Div(id="page-content"),
        html.Div(
            dcc.Loading(
                type="cube",
                color="black",
                children=[html.Div(id="content-loader")]
            ),
            style={'position': 'fixed', "top": "50%", "left": "50%"}
        )
       
    ])
    #content = dcc.Loading(
    #    type="default",
    #    children=[html.Div(id="page-content")]
    #)
    return html.Div([dcc.Location(id="url"), sidebar, content], style={'height': '90vh'})

def register(app):
    @app.callback(Output("page-content","className"),Input("url", "pathname"))
    def loading_page_alpha(pathname):
        return "opacity-5"
    
    @app.callback([Output("content-loader","children"),Output("page-content","children")],
                  [Input("url", "pathname")])
    def loading_page_spinner(pathname):
        #print("main.loading_page_spinner()")
        if pathname == "/": layout = page_home.layout()
        elif pathname == "/total": layout = page_total.layout()
        #elif pathname == "/yearly": layout = page_yearly.layout()
        elif pathname == "/data": layout = page_data.layout()
        elif pathname == "/about": layout = page_about.layout()
        # If the user tries to reach a different page, return a 404 message
        else:
            layout = dbc.Jumbotron([
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised...")
            ])
        return [],layout
    
    @app.callback(Output("sidebar", "className"),Input("sidebar-toggle", "n_clicks"),State("sidebar", "className"))
    def toggle_classname(n, classname):
        #print("main.toggle_classname()")
        if n and classname == "":
            return "collapsed"
        return ""
    
    @app.callback(Output("collapse", "is_open"),Input("navbar-toggle", "n_clicks"),State("collapse", "is_open"))
    def toggle_collapse(n, is_open):
        #print("main.toggle_collapse()")
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("download-data-csv", "data"),
        Input("btn_csv", "n_clicks"),
        prevent_initial_call=True,
    )
    def download_data(n_clicks):
        print("download_data()")
        x = config.data.cyklo()
        print(x)
        return dcc.send_data_frame(x.to_csv, "data.csv")