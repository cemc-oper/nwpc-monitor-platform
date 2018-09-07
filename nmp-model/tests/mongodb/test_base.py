# coding: utf-8
from datetime import datetime
from mongoengine import connect, EmbeddedDocument, StringField
import mongoengine
import pytest

from nmp_model.mongodb.base import Base


class FunnyData(EmbeddedDocument):
    value = StringField()


class TestBase(object):
    def setup_method(self):
        self.db_client = connect('mongoenginetest', host='mongomock://localhost')

    def teardown_method(self):
        self.db_client.close()

    def test_construction(self):
        base_object = Base()

        base_object = Base(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0)
        )

    def test_set_data(self):
        base_object = Base()

        data = FunnyData(
            value="foo"
        )
        base_object.set_data(data)

        data = {}
        with pytest.raises(TypeError):
            base_object.set_data(data)

    def test_is_valid(self):
        base_object = Base()
        assert base_object.is_valid() is False

        base_object = Base(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0)
        )
        assert base_object.is_valid() is True

    def test_to_dict(self):
        base_object = Base(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0)
        )

        base_dict = {
            'ticket_id': 1,
            'owner': 'owner',
            'repo': 'repo',
            'timestamp': datetime(2018, 9, 5, 11, 29, 0),
            'data': None
        }
        assert base_object.to_dict() == base_dict

    def test_save_to_db(self):
        base_object = Base(
            ticket_id=1
        )

        with pytest.raises(mongoengine.errors.InvalidDocumentError):
            base_object.save()
