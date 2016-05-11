#!/usr/bin/env python
from __future__ import absolute_import
from nwpc_monitor_task_scheduler.celery_server import tasks


def main():
    # result = tasks.get_group_sms_log_task.delay()
    #result = tasks.get_group_sms_status_task.delay()
    result = tasks.update_dingtalk_token_task.delay()
    print result

if __name__ == "__main__":
    main()
