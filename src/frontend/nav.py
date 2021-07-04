
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

def layout():
    sidebar = html.Div([
        dbc.Row([
            dbc.Col([
                html.H1("Jura jede")
            ], className="display-8", style={'paddingBottom': '5vh'})
        ]),
        dbc.Nav([
            dbc.NavLink("Domů",#"Home",
                        href="/", active="exact"),
            dbc.NavLink("Celkem",#"Total",
                        href="/total", active="exact"),
            dbc.NavLink("Ročně",#"Yearly",
                        href="/yearly", active="exact"),
            dbc.NavLink("Data", href="/data", active="exact"),
        ], vertical=True, pills=True)
    ], id="sidebar")
    return sidebar

