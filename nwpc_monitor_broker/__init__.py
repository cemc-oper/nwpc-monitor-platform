# coding=utf-8
from flask import Flask


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'windroc-nwpc-project'

from api import api_app
app.register_blueprint(api_app, url_prefix="/api/v1")
app.debug=True

from nwpc_monitor_broker import controller

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5101)