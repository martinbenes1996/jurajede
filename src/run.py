
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

# create app
app = create_light_app()
# set layout
app.layout = frontend.layout()
# initialize frontend
import data
frontend.register(app, data.cyklo.load)
#server = app.server

# run server
if __name__ == '__main__':
    app.run_server(debug=False)