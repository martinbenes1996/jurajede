
from . import chart_indicators

from . import chart_gauge_month
from . import chart_trace_year
from . import chart_pie_months
from . import chart_contour_years
from . import chart_gauge_total
from . import chart_series_total

def register(app):
    chart_indicators.register(app)
    
    chart_gauge_month.register(app)
    chart_trace_year.register(app)
    chart_pie_months.register(app)
    chart_contour_years.register(app)
    chart_gauge_total.register(app)
    chart_series_total.register(app)