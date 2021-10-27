
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from . import config
from . import chart_contour_years
from . import chart_series_total
from . import chart_indicators

def layout():
    def create_card(*args, **kw):
        return dbc.Card(dbc.CardBody(*args, className="text-center"), **kw)
    # indicators
    def create_indicator(figure, id):
        return create_card([
            chart_indicators.indicator_title[id[10:]],
            dcc.Graph(figure=figure, id=id, style={'height': '4rem'})
        ])
    indicatorKmTotal = create_indicator(chart_indicators.plot('km-total'), 'indicator-km-total')
    indicatorDaysTotal = create_indicator(chart_indicators.plot('days-total'), 'indicator-days-total')
    equatorsTotal = create_indicator(chart_indicators.plot('equators-total', '.4f'), 'indicator-equators-total')
    # plots
    traceYear = dcc.Graph(figure=chart_series_total.total(), id='trace-year')
    contourYears = dcc.Graph(figure=chart_contour_years.years(), id='contour-years', style={'height': '80vh'})
    # this month
    now = config.data.this_month()
    this_month = datetime.strptime('%04d-%02d-01' % now, '%Y-%m-%d')
    return html.Div([
        # header
        dbc.Row([
            dbc.Col([
                html.H2('Jura jede')
            ], className="text-center")
        ], className="contentHeader"),
        # total series
        traceYear,
        dbc.Tooltip(
            "Historie měsíčních kilometrů od roku 1992.",
            target="trace-year"
        ),
        # indicators
        dbc.CardDeck([
            indicatorKmTotal,
            equatorsTotal,
            indicatorDaysTotal
        ]),
        # contour
        contourYears,
        dbc.Tooltip(
            "Historie měsíčních kilometrů podél let.",
            target="contour-years"
        ),
        dbc.Row([     
            dbc.Col([
                dcc.RangeSlider(
                    id='series-type-slider',
                    min=config.total.min(),
                    max=config.total.max(),
                    value=[config.total.default(index=True)],
                    pushable=2,
                    marks={i:label for i,label in enumerate(config.total.labels())},
                    persistence = False
                )
            ], width=9),#, style={'width': '60%', 'display': 'inline-block', 'paddingTop': '3vh', 'paddingBottom': '3vh'}),
            dbc.Col([
                config.format_month_year(this_month)
            ], width=3, style={'textAlign': 'right'})
        ], style={'paddingTop': '2vh', 'paddingBottom': '2vh'})#,
    ])
