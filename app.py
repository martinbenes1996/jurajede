import os
import sys
sys.path.append('src')
from application import setup_app

def run(*args, **kw):
    app = setup_app()
    app.run_server(*args, **kw)
    
if __name__ == '__main__':
    app = setup_app()
    port = os.environ.get("PORT", 33507)
    app.run_server(host="0.0.0.0", port=port, debug=True)