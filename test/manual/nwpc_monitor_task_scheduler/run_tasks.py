#!/usr/bin/env python
from __future__ import absolute_import
import os
import sys

sys.path.append(os.path.dirname(__file__)+"/../../../")

def main():
    os.environ['MODE']='develop'
    from nwpc_monitor_task_scheduler.celery_server import tasks

    result = tasks.get_group_sms_status_task.delay()
    #result = tasks.update_dingtalk_token_task.delay()

    print result

if __name__ == "__main__":
    main()
