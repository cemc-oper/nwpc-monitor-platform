# coding=utf-8
import datetime
import json
import gzip
import requests

broker_host = "10.28.32.175"
broker_port = "6221"


def add_job(
        items,
        id=-1,
        owner="owner",
        job_class="job_class",
        queue_date=datetime.datetime.utcnow()):
    items.append({
        "props": [
            {
                "id": "llq.id",
                "data": "llq.id" + str(id),
                "text": "llq.id" + str(id),
                "value": "llq.id" + str(id)
            },
            {
                "id": "llq.owner",
                "data": owner,
                "text": owner,
                "value": owner
            },
            {
                "id": "llq.class",
                "data": job_class,
                "text": job_class,
                "value": job_class
            },
            {
                "id": "llq.job_script",
                "data": "llq.job_script" + str(id),
                "text": "llq.job_script" + str(id),
                "value": "llq.job_script" + str(id)
            },
            {
                "id": "llq.status" + str(id),
                "data": "llq.status" + str(id),
                "text": "llq.status" + str(id),
                "value": "llq.status" + str(id)
            },
            {
                "id": "llq.queue_date",
                "data": queue_date.strftime("%Y-%m-%d %H:%M:%S"),  # 2017-04-21 07:08:43
                "text": queue_date.strftime("%m/%d %H:%M"),  # "04/21 07:08",
                "value": queue_date.strftime("%a %b %d %H:%M:%S %Y"),  # "Fri Apr 21 07:08:43 2017"
            },
            {
                "id": "llq.priority",
                "data": id,
                "text": "llq.priority" + str(id),
                "value": "llq.priority" + str(id)
            }
        ]
    }
    )


def add_normal_job(items):
    cur_index = len(items) + 1
    job_queue_date_datetime = datetime.datetime.utcnow() - datetime.timedelta(hours=2)

    add_job(items,
            id=cur_index,
            owner="nwp",
            queue_date=job_queue_date_datetime)


def add_early_job(items):
    cur_index = len(items) + 1
    job_queue_date_datetime = datetime.datetime.utcnow() - datetime.timedelta(days=2)
    add_job(items, cur_index,
            owner="nwp",
            queue_date=job_queue_date_datetime)


def test_api():
    post_url = "http://{broker_host}:{broker_port}/api/v2/hpc/users/nwp_xp/loadleveler/status".format(
        broker_host=broker_host,
        broker_port=broker_port
    )
    items = []
    add_normal_job(items)
    add_early_job(items)
    message = {
        "time": "2017-04-21 07:08:45",
        "app": "nwpc_hpc_collector.loadleveler_status",
        "data": {
            "request": {
                "sub_command": "collect"
            },
            "response": {
                "items": items
            }
        },
        "type": "command"
    }

    post_data = {
        "message": json.dumps(message)
    }

    gzipped_post_data = gzip.compress(bytes(json.dumps(post_data), 'utf-8'))
    print('gzip the data...done')
    response = requests.post(
        post_url,
        data=gzipped_post_data,
        headers={
            'content-encoding': 'gzip'
        },
        timeout=60
    )
    print(response)


if __name__ == "__main__":
    test_api()
