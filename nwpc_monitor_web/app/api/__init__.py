# coding=utf-8
from flask import Blueprint

api_app = Blueprint('api_app', __name__, template_folder='template')

import nwpc_monitor_web.app.api.api_sms
import nwpc_monitor_web.app.api.api_hpc
import nwpc_monitor_web.app.api.api_test
