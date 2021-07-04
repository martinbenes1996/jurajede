
from . import config
from . import charts
from . import main

def layout():
    return main.layout()

def register(app, src):
    config.register(app, src)
    main.register(app)
    charts.register(app)
    
