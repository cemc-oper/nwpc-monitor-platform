# coding=utf-8
from nwpc_monitor_web import app

from flask import json, request, jsonify,render_template


@app.route('/')
def get_index_page():
    return render_template("index.html")