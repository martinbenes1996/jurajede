
import dash
from datetime import datetime
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
    km_now = float(x.tail(1).km)
    month_now = int(x.tail(1).month)
    month_now_name = datetime.strftime(datetime.strptime('2020-%02d-01'%month_now,'%Y-%m-%d'),'%B')
    km_past_mean = x[x.month == month_now]\
        .drop(x.index[x.shape[0]-1])\
        .km\
        .mean()
    # create plot
    fig = go.Figure(
        go.Indicator(
            domain = {'x': [0, 1], 'y': [0, 1]},
            value = km_now,
            mode = "gauge+number+delta",
            title = {'text': "Měsíc v historii {month_now_name}"},#f"Month in {month_now_name} history"},
            delta = {'reference': km_past_mean, 'relative': True},
            gauge = {
                'bar': {'color': "green" if km_past_mean < km_now else "red"},
                'axis': {'range': [None, max(km_now,km_past_mean)]},
                'steps' : [{'range': [0,km_past_mean], 'color': '#aaaaaa'}],
                'threshold' : {'line': {'color': "black", 'width': 2}, 'thickness': 1, 'value': km_past_mean}
            }
        )
    )
    fig.update_layout(**config.style.layout())
    return fig

def register(app):
    @app.callback(
        dash.dependencies.Output('gauge-total', 'figure'),
        dash.dependencies.Input('history-size-slider', 'value'),
        prevent_initial_call=True
    )
    def get_plot(index):
        print("chart_gauge_total.get_plot()")
        history_size = config.history.size(index)
        return create_plot(history_size)
    
    
def total():
    return create_plot(config.history.default())
