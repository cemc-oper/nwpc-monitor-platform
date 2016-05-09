# coding=utf-8
import os
from flask import Flask
from .config import Config, load_config

app = Flask(__name__)

app.config.from_object(load_config())

from api import api_app
app.register_blueprint(api_app, url_prefix="/api/v1")

from nwpc_monitor_broker import controller

if __name__ == "__main__":
    app.run(
        host=app.config.BROKER_CONFIG['host']['ip'],
        port=app.config.BROKER_CONFIG['host']['port']
    )