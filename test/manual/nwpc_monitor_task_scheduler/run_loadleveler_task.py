# coding=utf-8
import os
import sys

import nmp_scheduler.celery_server.task.workload.loadleveler

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
    nmp_scheduler.celery_server.task.workload.loadleveler.get_hpc_loadleveler_usage(param)


if __name__ == "__main__":
    test_loadleveler_task()
