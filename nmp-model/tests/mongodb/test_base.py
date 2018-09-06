# coding: utf-8
from datetime import datetime
from nmp_model.mongodb.base import Base


class TestBase(object):
    def test_construction(self):
        base_object = Base()

        base_object = Base(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0)
        )

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
