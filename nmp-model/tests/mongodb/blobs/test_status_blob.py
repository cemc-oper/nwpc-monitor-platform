# coding: utf-8
from datetime import datetime
from mongoengine import connect

from nmp_model.mongodb.blob import Blob
from nmp_model.mongodb.blobs.status import StatusBlob, StatusContent, StatusBlobData


class TestStatusContent(object):
    def test_construct(self):
        status_content = StatusContent()

        status_content = StatusContent(
            collected_time=datetime(2018, 9, 7, 10, 10, 12),
            update_time=datetime(2018, 9, 7, 10, 18, 12),
            status={
                'status': 'complete'
            }
        )

    def test_to_dict(self):
        status_content = StatusContent(
            collected_time=datetime(2018, 9, 7, 10, 10, 12),
            update_time=datetime(2018, 9, 7, 10, 18, 12),
            status={
                'status': 'complete'
            }
        )

        status_content_dict = {
            'collected_time': datetime(2018, 9, 7, 10, 10, 12),
            'update_time': datetime(2018, 9, 7, 10, 18, 12),
            'status': {
                'status': 'complete'
            }
        }

        assert status_content.to_dict() == status_content_dict


class TestStatusBlob(object):
    def test_construct(self):
        status_blob = StatusBlob()

        status_blob = StatusBlob(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0),
            data=StatusBlobData(
                name='sms_server_status',
                content=StatusContent(
                    collected_time=datetime.utcnow(),
                    update_time=datetime.utcnow(),
                    status={
                        'node': 'root',
                        'status': 'queue'
                    }
                )
            )
        )

    def test_to_dict(self):
        status_blob = StatusBlob(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0),
            data=StatusBlobData(
                name='sms_server_status',
                content=StatusContent(
                    collected_time=datetime(2018, 9, 7, 10, 10, 12),
                    update_time=datetime(2018, 9, 7, 10, 18, 12),
                    status={
                        'status': 'complete'
                    }
                )
            )
        )

        status_blob_dict = {
            'ticket_id': 1,
            'owner': 'owner',
            'repo': 'repo',
            'timestamp': datetime(2018, 9, 5, 11, 29, 0),
            'data': {
                'name': 'sms_server_status',
                'type': 'StatusBlobData',
                'content': {
                    'collected_time': datetime(2018, 9, 7, 10, 10, 12),
                    'update_time': datetime(2018, 9, 7, 10, 18, 12),
                    'status': {
                        'status': 'complete'
                    }
                }
            }
        }
        assert status_blob.to_dict() == status_blob_dict

    def test_save(self):
        status_blob = StatusBlob(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0),
            data=StatusBlobData(
                name='sms_server_status',
                content=StatusContent(
                    collected_time=datetime.utcnow(),
                    update_time=datetime.utcnow(),
                    status={
                        'node': 'root',
                        'status': 'queue'
                    }
                )
            )
        )
        connect('mongoenginetest', host='mongomock://localhost')
        status_blob.save()

        query_objects = Blob.objects(__raw__={'data._cls': 'StatusBlobData'}).all()
        assert len(query_objects) == 1
