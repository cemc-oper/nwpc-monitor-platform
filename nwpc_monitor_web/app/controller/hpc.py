# coding=utf-8
import datetime
from nwpc_monitor_web.app import app, redis_client, mongodb_client
from nwpc_work_flow_model.sms.visitor import pre_order_travel_dict, SubTreeNodeVisitor
from nwpc_monitor_web.app.common.operation_system import owner_list, get_owner_repo_status


from flask import json, request, jsonify, render_template, send_from_directory

nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop


@app.route('/hpc/nwp_xp/disk/usage', methods=['GET'])
def get_hpc_disk_usage():
    return render_template('app/hpc_app_index.html')
