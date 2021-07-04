
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from . import config
from . import chart_contour_years
from . import chart_series_total
from . import chart_indicators

def layout():
    def create_card(*args, **kw):
        return dbc.Card(dbc.CardBody(*args), **kw)
    # indicators
    def create_indicator(figure, id):
        return create_card(
            dcc.Graph(figure=figure, id=id, style={'height': '4rem'})
        )
    indicatorKmTotal = create_indicator(chart_indicators.plot('km-total'), 'indicator-km-total')
    indicatorDaysTotal = create_indicator(chart_indicators.plot('days-total'), 'indicator-days-total')
    equatorsTotal = create_indicator(chart_indicators.plot('equators-total', '.4f'), 'indicator-equators-total')
    
    return html.Div([
        html.Div([     
            html.Div([
                dcc.RangeSlider(
                    id='series-type-slider',
                    min=config.total.min(),
                    max=config.total.max(),
                    value=[config.total.default(index=True)],
                    pushable=2,
                    marks={i:label for i,label in enumerate(config.total.labels())},
                    persistence = False
                )
            ], style={'width': '60%', 'display': 'inline-block', 'paddingTop': '3vh', 'paddingBottom': '3vh'}),
            dbc.Row(
                dbc.Col(
                    html.H5('Celkem')#'Total')
                )
            ),
            dbc.Row(
                dbc.Col(
                    "Od roku 1992"
                )
            ),
            dbc.CardDeck([
                indicatorKmTotal,
                equatorsTotal,
                indicatorDaysTotal
            ]),
            dbc.CardDeck([
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph(figure=chart_series_total.total(), id='series-total')
                    ])
                )
            ]),
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