
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from . import config
from . import chart_contour_years

def layout():
    #fig = px.scatter(x=[config.history.current()], y=[1])
    #fig = go.Figure()
    #fig.add_trace(go.Scatter(x=[config.history.current()], y=[1]))
    
    return html.Div([
        html.Div([      
            html.Div([
                dcc.RangeSlider(
                    id='yearly-type-slider',
                    min=config.yearly.min(),
                    max=config.yearly.max(),
                    value=[config.yearly.default(index=True)],
                    pushable=2,
                    marks={i:label for i,label in enumerate(config.yearly.labels())},
                    persistence = False
                )
            ], style={'width': '60%', 'display': 'inline-block', 'paddingTop': '3vh', 'paddingBottom': '3vh'}),
            dbc.CardDeck([
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph(figure=chart_contour_years.years(),
                                  style={'height': '80vh'}, id='contour-years')
                    ])
                )
            ])
        ])
    ])
