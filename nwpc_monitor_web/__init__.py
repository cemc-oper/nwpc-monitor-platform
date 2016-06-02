# coding=utf-8

from flask import Flask
from flask.json import JSONEncoder
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, time, timedelta, date
from .config import load_config

app = Flask(__name__)

app.config.from_object(load_config())

class NwpcMonitorWebApiJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat(' ')  # obj.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        elif isinstance(obj, timedelta):
            return {'day': obj.days, 'seconds': obj.seconds}
        return JSONEncoder.default(self, obj)

app.json_encoder = NwpcMonitorWebApiJSONEncoder

#from nwpc_monitor.model import *
# db = SQLAlchemy(app)

from .api import api_app
app.register_blueprint(api_app, url_prefix="/api/v1")

import nwpc_monitor_web.controller