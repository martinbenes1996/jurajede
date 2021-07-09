
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime
from . import config

def layout():
    # this month
    now = config.data.this_month()
    this_month = datetime.strptime('%04d-%02d-01' % now, '%Y-%m-%d')
    # sidebar
    sidebar = html.Div([
        dbc.Button("Menu", id="sidebarCollapse", color="light", size="sm"),
        html.Div([
            html.Ul([
                html.Li([
                    dbc.NavLink("Domů", href="/", active="exact"),
                    dbc.NavLink("Celkem", href="/total", active="exact"),
                    dbc.NavLink("Bio", href="/about", active="exact"),
                    dbc.NavLink("Data", href="/data", active="exact"),
                    dbc.NavLink("Nastavení", href="/setting", active="exact"),
                ])
            ], className="list-unstyled components"),
        ]),
        html.Div([
            config.format_month_year(this_month)
        ], style={'textAlign': 'right'}, id="sidebarDate")  
    ], #className="active",
        id="sidebar")
    
    return sidebar
