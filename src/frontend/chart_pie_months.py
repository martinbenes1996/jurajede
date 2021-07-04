
import dash
from datetime import datetime
import numpy as np
import plotly.graph_objects as go
from . import config

def get_data(history_size):
    # read data
    x = config.data.cyklo()
    # crop
    year_max = x.year.max()
    year_min = max(x.year.min(), year_max - history_size)
    x = x[(x.year >= year_min) & (x.year <= year_max)]
    return x

def create_plot(history_size):
    # get data
    x = get_data(history_size)
    km_months = x\
        .groupby('month')\
        .aggregate({'km': 'mean'})\
        .reset_index()
    km_months['month_name'] = km_months.month.apply(
        lambda dt: datetime.strftime(datetime.strptime('2020-%02d-01'%dt,'%Y-%m-%d'),'%B')
    )
    # create plot
    fig = go.Figure(
        data=[go.Pie(labels=km_months.month_name, values=km_months.km, hole=0)]
    )
    fig.update_layout(**config.style.layout())
    return fig

def register(app):
    @app.callback(
        dash.dependencies.Output('pie-months', 'figure'),
        dash.dependencies.Input('history-size-slider', 'value'),
        prevent_initial_call=True
    )
    def get_plot(index):
        print("chart_pie_months.get_plot()")
        history_size = config.history.size(index)
        return create_plot(history_size)
    
    
def months():
    return create_plot(config.history.default())
