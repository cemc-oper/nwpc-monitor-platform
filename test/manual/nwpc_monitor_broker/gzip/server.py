from flask import Flask, request, jsonify, json
from flask.json import JSONEncoder
from datetime import datetime, time, timedelta, date
import gzip


app = Flask(__name__)


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


@app.route("/")
def hello():
    return "This page is used to test gzip on request body."


@app.route("/api/normal", methods=['POST'])
def get_normal_data():
    message = request.form['message']
    return jsonify({
        'status': 'ok'
    })


@app.route("/api/gzip", methods=['POST'])
def get_gzip_data():
    content_encoding = request.headers.get('content-encoding', '').lower()
    gzipped_data = request.data

    if content_encoding == 'gzip':
        print('decompress gzip data')
        data_string = gzip.decompress(gzipped_data)
        data = json.loads(data_string.decode('utf-8'))
        message = data['message']
    return jsonify({
        'status': 'ok'
    })


if __name__ == "__main__":
    app.run(port=6220)
