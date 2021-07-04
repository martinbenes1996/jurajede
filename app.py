import os
import sys
sys.path.append('src')
from application import setup_app

def run():
    app = setup_app()
    return app
    
if __name__ == '__main__':
    app = setup_app()
    port = os.environ.get("PORT", 33507)
    app.run_server(host="0.0.0.0", port=port, debug=True)