# coding: utf-8
from datetime import datetime

from nmp_model.mongodb.blobs.aborted_tasks import \
    AbortedTasksBlob, AbortedTasksBlobData, AbortedTasksContent, TaskStatusField


class TestStatusBlob(object):
    def test_construct(self):
        blob = AbortedTasksBlob()

        blob = AbortedTasksBlob(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0),
            data=AbortedTasksBlobData(
                name='sms_server_aborted_tasks',
                content=AbortedTasksContent(
                    status_blot_id=2,
                    tasks=[
                        TaskStatusField(
                            path='/f1/t1',
                            name='t1',
                            status='aborted'
                        ),
                        TaskStatusField(
                            path='/f2/t2',
                            name='t2',
                            status='aborted'
                        ),
                    ]
                )
            )
        )

        assert blob.ticket_id == 1
        # print(status_blob.to_dict())
