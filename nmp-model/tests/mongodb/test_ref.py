# coding: utf-8
from datetime import datetime
import pytest

from nmp_model.mongodb.ref import RefData, Ref


class TestRefData(object):
    def test_construction(self):
        ref_data = RefData()

        ref_data = RefData(
            key='v0.1',
            type='tree',
            id='2'
        )

        ref_data = RefData(
            key='v0.1',
            type='blob',
            id='2'
        )

        ref_data = RefData(
            key='v0.1',
            type='commit',
            id='2'
        )

    def test_to_dict(self):
        ref_data = RefData(
            key='v0.1',
            type='tree',
            id='2'
        )

        ref_data_dict = {
            'key': 'v0.1',
            'type': 'tree',
            'id': 2
        }

        assert ref_data.to_dict() == ref_data_dict


class TestRef(object):
    def test_construction(self):
        ref = Ref()

        ref = Ref(
            ticket_id=1,
            owner='my',
            repo='my_repo',
            timestamp=datetime(2018, 9, 17, 10, 9, 0),
            data=RefData(
                key='v0.1',
                type='tree',
                id='2'
            )
        )

    def test_set_data(self):
        ref = Ref(
            ticket_id=1,
            owner='my',
            repo='my_repo',
            timestamp=datetime(2018, 9, 17, 10, 9, 0)
        )

        ref_data = RefData(
            key='v0.1',
            type='tree',
            id='2'
        )

        ref.set_data(ref_data)

        ref_data = {}

        with pytest.raises(TypeError):
            ref.set_data(ref_data)

    def test_to_dict(self):
        ref = Ref(
            ticket_id=1,
            owner='my',
            repo='my_repo',
            timestamp=datetime(2018, 9, 17, 10, 9, 0),
            data=RefData(
                key='v0.1',
                type='tree',
                id='2'
            )
        )

        ref_dict = {
            'ticket_id': 1,
            'owner': 'my',
            'repo': 'my_repo',
            'timestamp': datetime(2018, 9, 17, 10, 9, 0),
            'data': {
                'key': 'v0.1',
                'type': 'tree',
                'id': 2
            }
        }

        assert ref.to_dict() == ref_dict
