# coding=utf-8
import os
import sys

sys.path.append(os.path.dirname(__file__)+"/../../../")
os.environ['MODE'] = 'develop'
from nmp_scheduler.celery_server.task.aix import hpc


def test_loadleveler_task():
    param = {
        'user': 'user',
        'password': 'password',
        'host': 'host',
        'port': 22
    }
    hpc.get_hpc_loadleveler_usage(param)


if __name__ == "__main__":
    test_loadleveler_task()
