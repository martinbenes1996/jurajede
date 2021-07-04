import dash
from dash.dependencies import Input, Output
from datetime import datetime
import logging
import math

class history:
    _sizes = [1,5,10,15,math.inf]
    _default = 1
    @classmethod
    def size(cls, current):
        current = current[0]
        return cls._sizes[current]
    @classmethod
    def default(cls, index=False):
        if not index: return cls.size([cls._default])
        else: return cls._default
    @classmethod
    def label(cls, current=None):
        if current is None: current = cls.default()
        else: current = current[0]
        if current == 1: return '1 rok'#'1 year'
        elif math.isinf(current): return 'Vše'#'All'
        #else: return '%d years' % current
        elif current < 5: return f'{current} roky'
        else: return f'{current} let'
    @classmethod
    def labels(cls):
        for size in cls._sizes:
            yield cls.label([size])
    @classmethod
    def len(cls): return len(cls._sizes)
    @classmethod
    def min(cls): return 0
    @classmethod
    def max(cls): return cls.len()-1
    #@classmethod
    #def index(cls, current = None):
    #    if current is None: current = cls._default
    #    else: current = current[0]
    #    for i,size in enumerate(cls._sizes):
    #        if current == size:
    #            return i
    #@classmethod
    #def annotation(cls, current = None):
    #    if current is None: current = cls._default
    #    else: current = current[0]
    #    return f'History: {cls.label(cls.current())}.'

class total:
    #_labels = ['Monthly', 'Daily (avg.)', 'Active', 'Idle']
    _labels = ['Měsíční', 'Denní (prům.)', 'Aktivní dny', 'Neaktivní']
    _attributes = ['km','km_p_day','days','days_off']
    _suffixes = {'km': ' km',
                 'km_p_day': ' km/den',#' km/day',
                 'km_p_activeday': ' km/aktivní den',#' km/active day',
                 'days': ' dní',#' days',
                 'days_off': ' dní',
                 'equators': ' rovníků'}#' equators'}
    _default = 0
    @classmethod
    def default(cls, index=False):
        if not index: return cls._labels[cls._default]
        else: return cls._default
    @classmethod
    def label(cls, current=None):
        if current is None: current = cls._default
        else: current = current[0]
        return cls._labels[current]
    @classmethod
    def attribute(cls, current=None):
        if current is None: current = cls._default
        else: current = current[0]
        return cls._attributes[current]
    @classmethod
    def suffix(cls, type):
        return cls._suffixes.get(type, '')
    @classmethod
    def labels(cls): return cls._labels
    @classmethod
    def size(cls): return len(cls._labels)
    @classmethod
    def min(cls): return 0
    @classmethod
    def max(cls): return cls.size() - 1

#class series:
#    #_labels = ['Monthly','Daily (avg.)','Activity'],
#    _labels = ['Měsíčně','Denně (prům.)','Aktivní dny']
#    _attributes = ['km','km_p_day','days']
#    _default = 0
#    @classmethod
#    def default(cls, index=False):
#        if not index: return cls._labels[cls._default]
#        else: return cls._default
#    @classmethod
#    def label(cls, current=None):
#        if current is None: current = cls._default
#        else: current = current[0]
#        return cls._labels[current]
#    @classmethod
#    def attribute(cls, current=None):
#        if current is None: current = cls._default
#        else: current = current[0]
#        return cls._attributes[current]
#    @classmethod
#    def labels(cls): return cls._labels
#    @classmethod
#    def size(cls): return len(cls._labels)
#    @classmethod
#    def min(cls): return 0
#    @classmethod
#    def max(cls): return cls.size() - 1

class indicators:
    #_types = {'km': 'Kilometers', 'km_p_day': 'Average daily kilometers', 'km_p_activeday': 'Average kilometers per active day', 'days': 'Days', 'equators': 'Earth equators'}
    _types = {'km': 'Kilometry', 'km_p_day': 'Průměrné denní kilometry', 'km_p_activeday': 'Průměr kilometrů na aktivní den', 'days': 'Dny', 'equators': 'Rovníky'}
    _suffixes = {'km': ' km',
                 'km_p_day': ' km/den',#' km/day',
                 'km_p_activeday': ' km/aktivní den',#' km/active day',
                 'days': ' dnů',#' days',
                 'equators': ' rovníků'}#' equators'}
    _prefixes = {'km_p_day': '~', 'km_p_activeday': '~'}
    @classmethod
    def types(cls): return list(cls._types.keys())
    @classmethod
    def title(cls, type):
        return cls._types[type]
    @classmethod
    def suffix(cls, type):
        return cls._suffixes.get(type, '')
    @classmethod
    def prefix(cls, type):
        return cls._prefixes.get(type, '')

def format_month(dt):
    #return datetime.strftime(dt, '%B %Y')
    cz_months = ['Leden','Únor','Březen','Duben','Květen','Červen',
                 'Červenec','Srpen','Září','Říjen','Listopad','Prosinec']
    month_id = int(datetime.strftime(dt, '%m'))
    return cz_months[month_id-1]

def format_month_year(dt):
    return f'{format_month(dt)} {datetime.strftime(dt, "%Y")}'  

class style:
    _figure_layout = {
        'template': 'plotly_light',
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)'
    }
    @classmethod
    def layout(cls):
        return cls._figure_layout
    @classmethod
    def set_dark(cls):
        cls._figure_layout['template'] = 'plotly_dark'
    @classmethod
    def set_light(cls):
        cls._figure_layout['template'] = 'plotly_white' # ggplot2 seaborn simple_white
        
class data:
    @classmethod
    def register(cls,src):
        cls._src = src
    @classmethod
    def cyklo(cls):
        return cls._src()
    @classmethod
    def this_month(cls):
        x = cls.cyklo()
        this_month = x.tail(1)
        return int(this_month.year), int(this_month.month)
    
def register(app, src):
    data.register(src)
