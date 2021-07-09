
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format,Scheme
import plotly.express as px
import plotly.graph_objects as go
from . import config

def get_data():
    # read data
    x = config.data.cyklo()
    x['km'] = x.km.astype(float)
    x.sort_values("date", ascending=False, inplace=True)
    return x

def get_table():
    x = get_data()
    int_format = {"type": "numeric",
                  "format": Format()}
    float_format = {"type": "numeric",
                    "format": Format(precision=2, scheme=Scheme.fixed)}
    columns = [
        {"id": "year", "name": "Rok",#"Year",
         **int_format},
        {"id": "month", "name": "Měsíc",#"Month",
         **int_format},
        {"id": "days", "name": "Aktivní dny",#"Active days",
         **int_format},
        {"id": "km", "name": "Kilometry",#"Kilometers",
         **float_format}
    ]
    return dash_table.DataTable(
        id='data',
        columns=columns,
        data=x.to_dict('records'),
    )

def layout():
    return dbc.Container([
        # header
        dbc.Row([
            dbc.Col([
                html.H2('Bio')
            ], className="text-center")
        ], className="contentHeader"),
        dbc.Row([
            dbc.Col([
                html.P([
                    "Já jsem Jura z Brna."
                ]),
                html.P([
                    "Druhý odstavec."
                ]),
                html.P([
                    "Třetí a poslední."
                ])  
            ], style={'textAlign': 'justify'})
        ])
    ])

