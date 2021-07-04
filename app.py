import logging
import os
import sys
sys.path.append('src')
from application import setup_app

# run production server
def run(*args, **kw):
    app = setup_app()
    logging.warning(str(args) + " " + str(kw))
    app.run_server(host=args[0]['SERVER_NAME'], port=args[0]['SERVER_PORT'])
    
# run debug server
#if __name__ == '__main__':
#    app = setup_app()
#    port = os.environ.get("PORT", 33507)
#    app.run_server(host="0.0.0.0", port=port, debug=True)