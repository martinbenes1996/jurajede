import logging
import os
import sys
sys.path.append('src')
from application import setup_app

# initialize app object
app = setup_app()
server = app.server

# run server
if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)
    app.run_server(host="0.0.0.0", port=port, debug=True)