
import dash
from datetime import datetime
import numpy as np
import plotly.graph_objects as go
from . import config

def get_data():
    # read data
    x = config.data.cyklo()
    # years
    x['year'] = x.date.apply(lambda d: int(datetime.strftime(d, '%Y')))
    # months
    months2020 = map(lambda month: datetime.strptime('2020-%02d-01'%month, "%Y-%m-%d"), range(1,13))
    monthsCZ = list(map(lambda month: config.format_month(month), months2020))
    x['monthCZ'] = x.date\
        .apply(lambda d: int(datetime.strftime(d, "%m")))\
        .apply(lambda d: monthsCZ[d-1])
    return x

def create_plot(attribute):
    # get data
    x = get_data()
    # date
    x['dateCZ'] = x.apply(lambda r: f'{r.monthCZ} {r.year}', axis=1)
    year_ticks = x[~x.year.duplicated()].reset_index(drop=True)
    year_ticks = year_ticks[(year_ticks.index == 0) | (year_ticks.year % 5 == 0)]
    # create plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x['dateCZ'], y=x[attribute],
            hovertemplate=
                "<b>%{x}</b><br>" +
                "%{y:.0f}"+config.total.suffix(attribute)+
                "<extra></extra>"
        )
    )
    fig.update_layout(**config.style.layout())
    fig.update_xaxes(
        ticktext=year_ticks.year,
        tickvals=year_ticks.dateCZ,
    )
    return fig

def register(app):
    @app.callback(
        dash.dependencies.Output('series-total', 'figure'),
        dash.dependencies.Input('series-type-slider', 'value'),
        prevent_initial_call=True
    )
    def get_plot(index):
        print("chart_series_total.get_plot()")
        #history_size = config.series.size(index)
        attribute = config.total.attribute(index)#'km' # use config and index
        return create_plot(attribute)
    
def total():
    return create_plot('km')#config.series.default())
