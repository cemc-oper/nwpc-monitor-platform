from flask import request, jsonify
import gzip
from nwpc_monitor_web.app.api import api_app


@api_app.route("/test/gzip")
def gzip_hello_page():
    return "This page is used to test gzip on request body."


@api_app.route("/test/gzip/normal", methods=['POST'])
def get_normal_data():
    message = request.form['message']
    return jsonify({
        'status': 'ok'
    })


@api_app.route("/api/gzip/compress", methods=['POST'])
def get_gzip_data():
    content_encoding = request.headers.get('content-encoding', '').lower()
    message = request.form['message']
    if content_encoding == 'gzip':
        print('decompress gzip data')
        message = gzip.decompress(message)
    return jsonify({
        'status': 'ok'
    })
