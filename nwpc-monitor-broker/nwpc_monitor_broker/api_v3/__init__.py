# coding=utf-8
from flask import Blueprint

api_v3_app = Blueprint('api_v3_app', __name__, template_folder='template')

import nwpc_monitor_broker.api_v3.server
import nwpc_monitor_broker.api_v3.workflow
import nwpc_monitor_broker.api_v3.util
import nwpc_monitor_broker.api_v3.alert
