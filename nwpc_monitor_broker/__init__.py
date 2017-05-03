# coding=utf-8

from flask import Flask
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time, timedelta, date
from .config import load_config

app = Flask(__name__)

app.config.from_object(load_config())


class NwpcMonitorBrokerApiJSONEncoder(JSONEncoder):
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

app.json_encoder = NwpcMonitorBrokerApiJSONEncoder

from werkzeug.routing import BaseConverter, ValidationError


class NoStaticConverter(BaseConverter):
    def to_python(self, value):
        if value == 'static':
            raise ValidationError()
        return value

    def to_url(self, value):
        return str(value)

app.url_map.converters['no_static'] = NoStaticConverter

db = SQLAlchemy(app)

from .api_v2 import api_v2_app
app.register_blueprint(api_v2_app, url_prefix="/api/v2")

from nwpc_monitor_broker import controller
