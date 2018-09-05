# coding: utf-8
from datetime import datetime

from nmp_model.mongodb.blob import BlobData
from nmp_model.mongodb.blobs.status import StatusBlob, StatusContent, StatusBlobData


class TestStatusBlob(object):
    def test_construct(self):
        status_blob = StatusBlob()

        status_blob = StatusBlob(
            id=1,
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

        assert status_blob.id == 1
        # print(status_blob.to_dict())
