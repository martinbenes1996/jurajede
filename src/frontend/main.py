
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from . import config
from . import nav
# pages
from . import page_about
from . import page_data
from . import page_home
from . import page_setting
from . import page_total


def layout():
    print("layout")
    sidebar = nav.layout()
    content = html.Div([
        html.Div(id="page-content-overlay"),
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
    return html.Div([dcc.Location(id="url"), sidebar, content], style={'height': '90vh'})

def register(app):
    
    @app.callback([Output("content-loader","children"),
                   Output("page-content","children")],
                  Input("url", "pathname"))
    def loading_page_spinner(pathname):
        print("loading_page_spinner:", pathname)
        if pathname == "/": layout = page_home.layout()
        elif pathname == "/total": layout = page_total.layout()
        elif pathname == "/data": layout = page_data.layout()
        elif pathname == "/about": layout = page_about.layout()
        elif pathname == "/setting": layout = page_setting.layout()
        # If the user tries to reach a different page, return a 404 message
        else:
            layout = dbc.Jumbotron([
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised...")
            ])
        return [],layout
    
    @app.callback([Output("sidebar", "className"),
                   Output("page-content-overlay", "className"),
                   Output("sidebarCollapse", "className")],
                  [Input("sidebarCollapse", "n_clicks"),
                   Input("page-content-overlay", "n_clicks"),
                   Input("url", "pathname")],
                  [State("sidebar", "className"),
                   State("page-content-overlay", "className")],
                  prevent_initial_call=True)
    def show_menu(n1, n2, pathname, classname1, classname2):
        print("show_menu:", pathname)
        #print("show_menu", n1, n2, classname1, classname2)
        is_active = classname1 == ""
        active_cls = "active" if is_active else ""
        button_cls = "btn-dark" if is_active else "btn-light"
        return active_cls, active_cls, button_cls                                                                                

    # download CSV
    @app.callback(
        Output("download-data-csv", "data"),
        Input("btn_csv", "n_clicks"),
        prevent_initial_call=True,
    )
    def download_data(n_clicks):
        print("download_data")
        x = config.data.cyklo()
        return dcc.send_data_frame(x.to_csv, "data.csv")
    