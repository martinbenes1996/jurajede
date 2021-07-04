
import dash
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
    
    #print(year_max, year_min)
    return x

def create_plot(history_size):
    # get data
    x = get_data(history_size)
    #print(x)
    this_year = float(x.tail(1).year)
    km_now = x[x.year == this_year]
    km_past = x[x.year != this_year]
    km_past_mean = km_past\
        .groupby(['month'])\
        .aggregate({'km': 'mean'})\
        .reset_index()
    def percentile(n):
        def percentile_(x):
            return np.percentile(x, n)
        percentile_.__name__ = 'percentile_%s' % n
        return percentile_
    km_past_ci = km_past\
        .groupby(['month'])\
        .km\
        .aggregate([percentile(2.5),percentile(97.5)])\
        .reset_index()
    # create plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=km_now.month, y=km_now.km, name="Tento rok")#"This year")
    )
    fig.add_trace(
        go.Scatter(x=km_past_mean.month, y=km_past_mean.km, name="Historie")#"History")
    )
    fig.add_trace(
        go.Scatter(
            x=np.concatenate((km_past_mean.month.to_numpy(),km_past_mean.month.to_numpy()[::-1])), # x, then x reversed
            y=np.concatenate((km_past_ci['percentile_2.5'].to_numpy(),km_past_ci['percentile_97.5'].to_numpy()[::-1])), # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        )
    )
    fig.update_layout(**config.style.layout())
    return fig

def register(app):
    @app.callback(
        dash.dependencies.Output('trace-year', 'figure'),
        dash.dependencies.Input('history-size-slider', 'value')
    )
    def get_plot(index):
        history_size = config.history.size(index)
        return create_plot(history_size)
    
def year():
    return create_plot(config.history.default())
