import os
import sys
sys.path.append('src')
from application import setup_app

app = setup_app()

if __name__ == '__main__':
    port = os.environ.get("PORT", 33507)
    app.run_server(host="0.0.0.0", port=port, debug=True)
    #run()