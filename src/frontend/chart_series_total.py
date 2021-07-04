
import dash
import numpy as np
import plotly.graph_objects as go
from . import config

def get_data():
    # read data
    x = config.data.cyklo()
    return x

def create_plot(attribute):
    # get data
    x = get_data()
    # create plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=x.date, y=x[attribute])
    )
    fig.update_layout(**config.style.layout())
    return fig

def register(app):
    @app.callback(
        dash.dependencies.Output('series-total', 'figure'),
        dash.dependencies.Input('series-type-slider', 'value')
    )
    def get_plot(index):
        #history_size = config.series.size(index)
        attribute = config.series.attribute(index)#'km' # use config and index
        return create_plot(attribute)
    
def total():
    return create_plot('km')#config.series.default())
