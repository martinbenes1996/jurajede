
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format,Scheme
import plotly.express as px
import plotly.graph_objects as go
from . import config

def layout():
    return dbc.Container([
        # header
        dbc.Row([
            dbc.Col([
                html.H2('Nastavení')
            ], className="text-center")
        ], className="contentHeader"),
        dbc.Row([
            dbc.Col([
                "Zobraz relativně k historii o délce",
                dcc.RangeSlider(
                    id='history-size-slider',
                    min=config.history.min(),
                    max=config.history.max(),
                    value=[config.history.default(index=True)],
                    pushable=2,
                    marks={i:label for i,label in enumerate(config.history.labels())},
                    persistence = False
                )
            ], style={'textAlign': 'justify'})
        ])
    ])

