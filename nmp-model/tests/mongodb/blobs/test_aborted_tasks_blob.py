# coding: utf-8
from datetime import datetime
from mongoengine import connect

from nmp_model.mongodb.blobs.aborted_tasks import \
    AbortedTasksBlob, AbortedTasksBlobData, AbortedTasksContent, TaskStatusField


class TestAbortedTasksContent(object):
    def test_construct(self):
        content = AbortedTasksContent()

        content = AbortedTasksContent(
            status_blob_id=2,
            server_name='nwpc_op',
            collected_time=datetime(2018, 9, 19, 11, 4, 0),
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
        assert len(content.tasks) == 2

    def test_to_dict(self):
        content = AbortedTasksContent(
            status_blob_id=2,
            server_name='nwpc_op',
            collected_time=datetime(2018, 9, 19, 11, 4, 0),
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

        content_dict = {
            'status_blob_id': 2,
            'server_name': 'nwpc_op',
            'collected_time': datetime(2018, 9, 19, 11, 4, 0),
            'tasks': [
                {
                    'path': '/f1/t1',
                    'name': 't1',
                    'status': 'aborted'
                },
                {
                    'path': '/f2/t2',
                    'name': 't2',
                    'status': 'aborted'
                }
            ]
        }

        assert content.to_dict() == content_dict


class TestAbortedTasksBlob(object):

    def test_construct(self):
        blob = AbortedTasksBlob()

        blob_data = AbortedTasksBlobData(
            name='sms_server_aborted_tasks',
            content=AbortedTasksContent(
                status_blob_id=2,
                server_name='nwpc_op',
                collected_time=datetime(2018, 9, 19, 11, 4, 0),
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

        blob = AbortedTasksBlob(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0),
            data=blob_data
        )

        assert blob.ticket_id == 1

    def test_save(self):
        blob_data = AbortedTasksBlobData(
            name='sms_server_aborted_tasks',
            content=AbortedTasksContent(
                status_blob_id=2,
                server_name='nwpc_op',
                collected_time=datetime(2018, 9, 19, 11, 4, 0),
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

        blob = AbortedTasksBlob(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0),
            data=blob_data
        )

        connect('mongoenginetest', host='mongomock://localhost')
        blob.save()

        query_objects = AbortedTasksBlob.objects(__raw__={'data._cls': 'AbortedTasksBlobData'}).all()
        assert len(query_objects) == 1
