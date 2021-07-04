import os
import sys
sys.path.append('src')
from application import setup_app

def run():
    app = setup_app()
    app.run_server(host="0.0.0.0", port=os.environ.get("PORT", 5000), debug=True)

#if __name__ == '__main__':
#    app = setup_app()
#    app.run_server(debug=True)