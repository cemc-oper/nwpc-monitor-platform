# coding=utf-8
import requests
import sys
import os
import json
import datetime
import gzip

# normal_url = 'http://127.0.0.1:6220/api/normal'
# gzip_url = 'http://127.0.0.1:6220/api/gzip'

normal_url = 'https://www.nwpcmonitor.cc/api/test/gzip/normal'
gzip_url = 'https://www.nwpcmonitor.cc/api/test/gzip/compress'


def send_normal(data_file_path):
    with open(data_file_path, 'r') as f:
        print("reading file...")
        content = f.read()
        print("reading file...done")
        json_content = json.loads(content)
        message_content = json.dumps(json_content)

        start_time = datetime.datetime.now()
        result = requests.post(normal_url, data={
            'message': message_content
        })
        end_time = datetime.datetime.now()
        print(len(message_content))
        return end_time - start_time


def send_gzip(data_file_path):
    with open(data_file_path, 'r') as f:
        print("reading file...")
        content = f.read()
        print("reading file...done")
        json_content = json.loads(content)
        message_content = json.dumps(json_content)

        start_time = datetime.datetime.now()
        message_gzip_content = gzip.compress(bytes(message_content, 'utf8'))
        result = requests.post(gzip_url, data={
            'message': message_gzip_content
        })
        end_time = datetime.datetime.now()

        print(len(message_gzip_content))
        return end_time - start_time


if __name__ == "__main__":

    file_path = os.path.join(os.path.dirname(__file__), 'data_nwp.json')
    print(send_normal(file_path))
    print(send_gzip(file_path))
