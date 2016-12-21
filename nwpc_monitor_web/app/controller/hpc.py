# coding=utf-8
from nwpc_monitor_web.app import app
from flask import render_template


@app.route('/hpc/nwp_xp/disk/usage', methods=['GET'])
def get_hpc_disk_usage():
    return render_template('app/hpc_app_index.html')


@app.route('/hpc/nwp_xp/loadleveler/status', methods=['GET'])
def get_hpc_loadleveler_status():
    return render_template('app/hpc_app_index.html')
