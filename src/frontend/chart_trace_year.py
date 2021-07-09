
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
    x = x.sort_values("date")
    # cz month
    x['monthCZ'] = x.month\
        .apply(lambda m: datetime.strptime("2020-%02d-01" % (m,), "%Y-%m-%d"))\
        .apply(config.format_month)
    return x

def create_plot(history_size):
    # get data
    x = get_data(history_size)
    this_year = float(x.tail(1).year)
    km_now = x[x.year == this_year]
    km_past = x[x.year != this_year]
    # mean
    km_past_mean = km_past\
        .groupby(['month','monthCZ'])\
        .aggregate({'km': 'mean'})\
        .reset_index()
    # ci
    def percentile(n):
        def percentile_(x):
            return np.percentile(x, n)
        percentile_.__name__ = 'percentile_%s' % n
        return percentile_
    km_past_ci = km_past\
        .groupby(['month','monthCZ'])\
        .km\
        .aggregate([percentile(2.5),percentile(97.5)])\
        .reset_index()
    # months
    month_ticks = km_past_mean.monthCZ[km_past_mean.monthCZ.index.isin({0,6,11})]
    # create plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=km_now.monthCZ, y=km_now.km, name="Tento rok")
    )
    fig.add_trace(
        go.Scatter(x=km_past_mean.monthCZ, y=km_past_mean.km, name="Historie")
    )
    fig.add_trace(
        go.Scatter(
            x=np.concatenate((km_past_mean.monthCZ.to_numpy(),km_past_mean.monthCZ.to_numpy()[::-1])), # x, then x reversed
            y=np.concatenate((km_past_ci['percentile_2.5'].to_numpy(),km_past_ci['percentile_97.5'].to_numpy()[::-1])), # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        )
    )
    fig.update_layout(hovermode="x unified", **config.style.layout())
    fig.update_yaxes(ticklabelposition="inside top", title=None)
    fig.update_xaxes(ticklabelposition="inside", title=None,
                     ticktext=month_ticks, tickvals=month_ticks)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=1,
        xanchor="right",
        x=1
    ))
    return fig

def register(app):
    @app.callback(
        dash.dependencies.Output('trace-year', 'figure'),
        dash.dependencies.Input('history-size-slider', 'value'),
        prevent_initial_call=True
    )
    def get_plot(index):
        print("chart_trace_year.get_plot()")
        history_size = config.history.size(index)
        return create_plot(history_size)
    
def year():
    return create_plot(config.history.default())
