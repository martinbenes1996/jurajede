
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
            x=months_names, y=years, z=z,
            hovertemplate=
                "<b>%{x} %{y}</b><br>" +
                "%{z:.0f}"+config.total.suffix(attribute)+
                "<extra></extra>",
            showscale=False
        )
    )
    fig.update_layout(**config.style.layout())
    return fig
    
def register(app):
    @app.callback(
        dash.dependencies.Output('contour-years', 'figure'),
        dash.dependencies.Input('series-type-slider', 'value'),
        prevent_initial_call=True
    )
    def get_plot(index):
        print("chart_contour_years.get_plot()")
        attribute = config.total.attribute(index)
        return create_plot(attribute)
    
    
def years():
    default_attribute = config.total.attribute()
    return create_plot(default_attribute) # default from config
