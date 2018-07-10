# coding=utf-8
from flask import Blueprint

api_v2_app = Blueprint('api_v2_app', __name__, template_folder='template')

import nwpc_monitor_broker.api_v2.api_sms
import nwpc_monitor_broker.api_v2.api_org
import nwpc_monitor_broker.api_v2.api_repo
import nwpc_monitor_broker.api_v2.api_hpc
import nwpc_monitor_broker.api_v2.api_nofitication
import nwpc_monitor_broker.api_v2.api_ecflow
