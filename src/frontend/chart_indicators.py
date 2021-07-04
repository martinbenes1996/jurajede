
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
    return x

def get_month_data(history_size):
    # read data
    x = config.data.cyklo()
    # crop
    year_max = x.year.max()
    year_min = max(x.year.min(), year_max - history_size)
    x = x[(x.year >= year_min) & (x.year <= year_max)]
    # now
    now = x.tail(1)
    past = x[x.month == int(now.month)]\
        .drop(x.index[x.shape[0]-1])
    return now,past

def create_month_indicator(history_size, attr):
    #print(f"Creating month indicator for {attr} with history {history_size}")
    # get data
    now,past = get_month_data(history_size)
    attr_name = config.indicators.title(attr)
    # now
    attr_now = float(now[attr])
    month_now = int(now.month)
    month_now_name = datetime.strftime(datetime.strptime('2020-%02d-01'%month_now,'%Y-%m-%d'),'%B')
    # past
    attr_past_mean = past[attr].mean()
    #print(f'month indicator {attr} with {attr_now}/{attr_past_mean}')
    # plot
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        #title = {"text": "Last month"},
        mode = "number+delta",
        value = attr_now,
        number = {'suffix': config.indicators.suffix(attr), 'font': {'size': 20}, 'prefix': config.indicators.prefix(attr)},
        delta = {'reference': attr_past_mean, 'relative': True, 'font': {'size': 10}}#,
        #domain = {'row': 0, 'column': 0}
    ))
    fig.update_layout(**config.style.layout())
    return fig

def create_total_indicator(history_size, attr, format=None):
    # get data
    x = get_data(history_size)
    attr_name = config.indicators.title(attr)
    # sum
    #if attr == 'km':
    #    print(x.km.to_numpy())
    value = float(
        x[[attr]]\
            .dropna()\
            .sum()
    )
    if format is None:
        value = int(value)
        format = 'ld'
    # plot
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        #title = {"text": "Last month"},
        mode = "number",
        value = value,
        number = {'valueformat': format, 'suffix': config.indicators.suffix(attr), 'font': {'size': 20}, 'prefix': config.indicators.prefix(attr)}
        #delta = {'reference': attr_past_mean, 'relative': True, 'font': {'size': 10}}#,
        #domain = {'row': 0, 'column': 0}
    ))
    fig.update_layout(**config.style.layout())
    return fig

def register(app):
    @app.callback(
        dash.dependencies.Output(f'indicator-km', 'figure'),
        dash.dependencies.Input('history-size-slider', 'value')
    )
    def _km(index):
        history_size = config.history.size(index)
        return create_month_indicator(history_size, 'km')
    @app.callback(
        dash.dependencies.Output(f'indicator-km_p_day', 'figure'),
        dash.dependencies.Input('history-size-slider', 'value')
    )
    def _km_p_day(index):
        history_size = config.history.size(index)
        return create_month_indicator(history_size, 'km_p_day')
    @app.callback(
        dash.dependencies.Output(f'indicator-km_p_activeday', 'figure'),
        dash.dependencies.Input('history-size-slider', 'value')
    )
    def _km_p_activeday(index):
        history_size = config.history.size(index)
        return create_month_indicator(history_size, 'km_p_activeday')
    @app.callback(
        dash.dependencies.Output('indicator-km-total', 'figure'),
        dash.dependencies.Input('history-size-slider', 'value')
    )
    def _km_total(index):
        history_size = config.history.size(index)
        return create_total_indicator(history_size, 'km')
    #@app.callback(
    #    dash.dependencies.Output('indicator-days-total', 'figure'),
    #    dash.dependencies.Input('history-size-slider', 'value')
    #)
    #def _km_total(index):
    #    history_size = config.history.size(index)
    #    return create_total_indicator(history_size, 'days')
    #@app.callback(
    #    dash.dependencies.Output('indicator-equators-total', 'figure'),
    #    dash.dependencies.Input('history-size-slider', 'value')
    #)
    #def _km_total(index):
    #    history_size = config.history.size(index)
    #    return create_total_indicator(-1, 'equators', '.4f')


def plot(type, format = None):
    type_list = type.split('-')
    if len(type_list) == 1:
        return create_month_indicator(config.history.default(), type)
    elif len(type_list) == 2 and type_list[1] == 'total':
        history_size = config.history.size([config.history.max()])
        return create_total_indicator(history_size, type_list[0], format)
        
