import sys
sys.path.append('src')
from application import setup_app

def run():
    app = setup_app()
    app.run_server(debug=True)

#if __name__ == '__main__':
#    app = setup_app()
#    app.run_server(debug=True)