
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format,Scheme
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from . import config

def get_data():
    # read data
    x = config.data.cyklo()
    # km
    x['km'] = x.km.astype(float)
    # months
    x.sort_values("date", ascending=False, inplace=True)
    months2020 = map(lambda month: datetime.strptime('2020-%02d-01'%month, "%Y-%m-%d"), range(1,13))
    monthsCZ = list(map(lambda month: config.format_month(month), months2020))
    x['monthCZ'] = x.date\
        .apply(lambda d: int(datetime.strftime(d, "%m")))\
        .apply(lambda d: monthsCZ[d-1])
    x['yearmonthCZ'] = x.apply(lambda r: f'{r.monthCZ} {r.year}', axis=1)
        
    return x

def get_table():
    x = get_data()
    int_format = {"type": "numeric",
                  "format": Format()}
    float_format = {"type": "numeric",
                    "format": Format(precision=2, scheme=Scheme.fixed)}
    columns = [
        #{"id": "year", "name": "Rok",#"Year",
        # **int_format},
        {"id": "yearmonthCZ", "name": "Měsíc",#"Month",
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
        page_size=18,
    )

def layout():
    return html.Div([
        # header
        
        dbc.Container([
            dbc.Row([
            dbc.Col([
                html.H2('Data')
            ], className="text-center")
        ], className="contentHeader"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("Download CSV", id="btn_csv", outline=True, color="dark", block=True),
                    dcc.Download(id="download-data-csv"),
                ], style={'textAlign': 'right',
                    'marginTop': '2rem', 'marginBottom': '2rem',
                    'marginLeft': '2rem', 'marginRight': '2rem'})
            ]),
            dbc.Row([
                dbc.Col(get_table())
            ], style={'textAlign': 'center'})
        ], fluid=True, style={'paddingLeft': '2rem'})
    ])