
import dash
import dash_bootstrap_components as dbc
from jupyter_dash import JupyterDash

import sys
sys.path.append('src')
import frontend

def create_app(sheet):
    return JupyterDash(
        __name__,
        external_stylesheets=[sheet], 
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
    )
def create_dark_app():
    frontend.config.style.set_dark()
    # Dark: DARKLY CYBORG SOLAR
    return create_app(dbc.themes.CYBORG)
def create_light_app():
    frontend.config.style.set_light()
    # Light: LUX FLATLY LUMEN SKETCHY JOURNAL SANDSTONE UNITED PULSE MINTY MATERIA SIMPLEX
    return create_app(dbc.themes.LUX)

def setup_app():
    # create app
    app = create_light_app()
    # initialize frontend
    import data
    frontend.register(app, data.cyklo.load)
    # set layout
    app.layout = frontend.layout()
    #server = app.server
    return app
    # run server
    

if __name__ == '__main__':
    app = setup_app()
    app.run_server(debug=True)
    