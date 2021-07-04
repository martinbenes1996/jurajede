
from datetime import datetime
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from . import config
from . import chart_indicators
from . import chart_gauge_month
from . import chart_trace_year
from . import chart_pie_months
from . import chart_gauge_total
    
def layout():
    def create_card(*args, **kw):
        return dbc.Card(dbc.CardBody(*args), **kw)
    # indicators
    def create_indicator(figure, id):
        return create_card(
            dcc.Graph(figure=figure, id=id, style={'height': '4rem'})
        )
    indicatorKm = create_indicator(chart_indicators.plot('km'), 'indicator-km')
    indicatorDailyKm = create_indicator(chart_indicators.plot('km_p_day'), 'indicator-km_p_day')
    indicatorActiveDailyKm = create_indicator(chart_indicators.plot('km_p_activeday'), 'indicator-km_p_activeday')
    # plots
    traceYear = create_card(dcc.Graph(figure=chart_trace_year.year(), id='trace-year'))
    #dcc.Graph(figure=chart_gauge_month.month(), id='gauge-monthly')
    #dcc.Graph(figure=chart_pie_months.months(), id='pie-months')
    #dcc.Graph(figure=chart_gauge_total.total(), id='gauge-total')
    #dcc.Graph(figure=chart_trace_year.year(), id='trace-year')
    # this month
    now = config.data.this_month()
    this_month = datetime.strptime('%04d-%02d-01' % now, '%Y-%m-%d')
    return html.Div([    
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
            ], width=8),
            dbc.Col([
                config.format_month_year(this_month)
            ], width=4, style={'textAlign': 'right'})
        ], style={'paddingTop': '2vh', 'paddingBottom': '2vh'}),
        dbc.Row(
            dbc.Col(
                html.H5('Výkon za tento měsíc')#'This month')
            )
        ),
        dbc.CardDeck([
            indicatorKm,
            indicatorDailyKm,
            indicatorActiveDailyKm
        ]),
        dbc.Row(
            dbc.Col(
                html.H5('Výkon za tento rok')#'This year')
            )
        ),
        dbc.Row(
            dbc.Col(
                "v kontextu klouzavého průměru posledních let a intervalu spolehlivosti 95%"
            )
        ),
        dbc.CardDeck([
            traceYear
        ])
    ])
    