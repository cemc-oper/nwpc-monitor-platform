# coding: utf-8
from datetime import datetime
from mongoengine import EmbeddedDocument, StringField, connect
import pytest

from nmp_model.mongodb.blob import BlobData, Blob


class FunnyData(EmbeddedDocument):
    value = StringField()


class FunnyContent(EmbeddedDocument):
    value = StringField()

    def to_dict(self):
        return {
            'value': self.value
        }


class TestBlobData(object):
    def test_construction(self):
        blob_data = BlobData()

        blob_data = BlobData(
            type='DefaultBlobData',
            name='default_blob_data',
            content=FunnyContent(
                value='string'
            )
        )

    def test_to_dict(self):
        blob_data = BlobData()
        assert blob_data.to_dict() == {
            'type': None,
            'name': None,
            'content': None
        }

        blob_data = BlobData(
            type='DefaultBlobData',
            name='default_blob_data',
            content=FunnyContent(
                value='my value'
            )
        )
        assert blob_data.to_dict() == {
            'type': 'DefaultBlobData',
            'name': 'default_blob_data',
            'content': {
                'value': 'my value'
            }
        }


class TestBlob(object):
    def setup_method(self):
        self.db_client = connect('mongoenginetest', host='mongomock://localhost')

    def teardown_method(self):
        self.db_client.close()

    def test_construction(self):
        blob = Blob()

        blob_data = BlobData(
            type='DefaultBlobData',
            name='default_blob_data',
            content=FunnyContent(
                value='my value'
            )
        )

        blob = Blob(
            ticket_id=1,
            owner='owner',
            repo='repo',
            data=blob_data
        )

        assert blob.ticket_id == 1
        assert blob.owner == 'owner'
        assert blob.repo == 'repo'
        assert blob.data == blob_data

    def test_set_data(self):
        blob = Blob()

        blob_data = BlobData(
            type='DefaultBlobData',
            name='default_blob_data',
            content=FunnyContent(
                value='my value'
            )
        )

        blob.set_data(blob_data)

        blob_data = FunnyData(
            value="foo"
        )
        with pytest.raises(TypeError):
            blob.set_data(blob_data)

    def test_to_dict(self):
        blob_data = BlobData(
            type='DefaultBlobData',
            name='default_blob_data',
            content=FunnyContent(
                value='my value'
            )
        )

        blob = Blob(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0),
            data=blob_data
        )

        blob_dict = {
            'ticket_id': 1,
            'owner': 'owner',
            'repo': 'repo',
            'timestamp': datetime(2018, 9, 5, 11, 29, 0),
            'data': {
                'type': 'DefaultBlobData',
                'name': 'default_blob_data',
                'content': {
                    'value': 'my value'
                }
            }
        }

        assert blob.to_dict() == blob_dict
