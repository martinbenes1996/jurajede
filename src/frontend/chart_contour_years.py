
import dash
from datetime import datetime
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
    # parse to matrix
    x = x[['year','month',attribute]]\
        .pivot(index='year',columns='month')\
        .sort_index(ascending=False)
    z = x.to_numpy()
    # time labels
    months = map(lambda month: datetime.strptime('2020-%02d-01'%month, "%Y-%m-%d"), range(1,13))
    months_names = list(map(lambda month: config.format_month(month), months))#datetime.strftime(month, "%B"), months))
    years = x.index
    # create plot
    fig = go.Figure(
        data=go.Contour(
            z=z,
            x=months_names,
            y=years
        )
    )
    fig.update_layout(**config.style.layout())
    return fig
    
def register(app):
    @app.callback(
        dash.dependencies.Output('contour-years', 'figure'),
        dash.dependencies.Input('yearly-type-slider', 'value')
    )
    def get_plot(index):
        attribute = config.yearly.attribute(index)
        return create_plot(attribute)
    
    
def years():
    default_attribute = config.yearly.attribute()
    return create_plot(default_attribute) # default from config
