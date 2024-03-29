#!/usr/bin/env python3
import os
import sys

import nmp_scheduler.celery_server.task.sms.status

sys.path.append(os.path.dirname(__file__)+"/../../../")

def main():
    os.environ['MODE']='develop'
    from nmp_scheduler.celery_server.task import sms

    result = nmp_scheduler.celery_server.task.sms.status.get_group_sms_status_task.delay()
    # result = tasks.update_dingtalk_token_task.delay()

    print(result)

if __name__ == "__main__":
    main()
