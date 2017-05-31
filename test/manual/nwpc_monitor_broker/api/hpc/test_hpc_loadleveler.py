import datetime
import json
import gzip
import requests


# TODO: repeat is evil
def create_job(
        job_id="id_no",
        owner="owner",
        job_class="job_class",
        queue_date=datetime.datetime.now(),
        status="R",
        priority=100
):
    return {
        "props": [
            {
                "id": "llq.id",
                "data": job_id,
                "text": job_id,
                "value": job_id
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
                "data": "llq.job_script" + job_id,
                "text": "llq.job_script" + job_id,
                "value": "llq.job_script" + job_id
            },
            {
                "id": "llq.status" + job_id,
                "data": status,
                "text": status,
                "value": status
            },
            {
                "id": "llq.queue_date",
                "data": queue_date.strftime("%Y-%m-%d %H:%M:%S"),  # 2017-04-21 07:08:43
                "text": queue_date.strftime("%m/%d %H:%M"),  # "04/21 07:08",
                "value": queue_date.strftime("%a %b %d %H:%M:%S %Y"),  # "Fri Apr 21 07:08:43 2017"
            },
            {
                "id": "llq.priority",
                "data": priority,
                "text": priority,
                "value": priority
            }
        ]
    }


def test_loadleveler_status_api():
    result = {
        'app': 'nwpc_hpc_collector.loadleveler_status',
        'type': 'command',
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'data': {
            'request': {
                'sub_command': 'collect',
            },
            'response': {
                'items': [
                    create_job(
                        owner="nwp",
                        queue_date=datetime.datetime.now() - datetime.timedelta(days=2)),
                    create_job(
                        owner="nwp",
                        queue_date=datetime.datetime.now() - datetime.timedelta(hours=2)),
                    create_job(
                        owner="nwp_qu",
                        queue_date=datetime.datetime.now() - datetime.timedelta(days=3)),
                    create_job(
                        owner="wangdp",
                        queue_date=datetime.datetime.now() - datetime.timedelta(days=2))
                ]
            }
        }
    }

    post_data = {
        'message': json.dumps(result)
    }

    gzipped_data = gzip.compress(bytes(json.dumps(post_data), 'utf-8'))
    url = 'http://10.28.32.175:6221/api/v2/hpc/users/{owner}/loadleveler/status'.format(
        owner='wangdp'
    )
    requests.post(url, data=gzipped_data, headers={
        'content-encoding': 'gzip'
    })


if __name__ == "__main__":
    test_loadleveler_status_api()
