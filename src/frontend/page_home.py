
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
        return dbc.Card(dbc.CardBody(*args, className="text-center"), **kw)
    # indicators
    def create_indicator(figure, id):
        return create_card([
            chart_indicators.indicator_title[id.split("-")[1]],
            dcc.Graph(figure=figure, id=id, style={'height': '4rem'})
        ])
    indicatorKm = create_indicator(chart_indicators.plot('km'), 'indicator-km')
    indicatorDailyKm = create_indicator(chart_indicators.plot('km_p_day'), 'indicator-km_p_day')
    indicatorActiveDailyKm = create_indicator(chart_indicators.plot('km_p_activeday'), 'indicator-km_p_activeday')
    # plots
    traceYear = dcc.Graph(figure=chart_trace_year.year(), id='trace-year')
    #dcc.Graph(figure=chart_gauge_month.month(), id='gauge-monthly')
    #dcc.Graph(figure=chart_pie_months.months(), id='pie-months')
    #dcc.Graph(figure=chart_gauge_total.total(), id='gauge-total')
    #dcc.Graph(figure=chart_trace_year.year(), id='trace-year')
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
        html.Div([ 
            # year trace
            traceYear,
            dbc.Tooltip(
                "Tento měsíc v kontextu klouzavého průměru posledních let a intervalu spolehlivosti 95%.",
                target="trace-year",
            ),
            # indicators
            dbc.CardDeck([
                indicatorKm,
                indicatorDailyKm,
                indicatorActiveDailyKm
            ]),
        ], id="dashboard-content")
    ])
    