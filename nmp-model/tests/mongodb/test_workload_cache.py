# coding: utf-8
from datetime import datetime

from nmp_model.mongodb.workload_cache import WorkloadCacheData, WorkloadCache


class TestWorkloadCacheData(object):
    def test_construction(self):
        data = WorkloadCacheData()

        data = WorkloadCacheData(
            server_name='nwpc_op',
            collected_time=datetime(2018, 9, 20, 9, 14, 0),
            update_time=datetime(2018, 9, 20, 9, 15, 0),
            status={
                'node': '/',
                'path': '/',
                'status': 'complete'
            }
        )

    def test_to_dict(self):
        data = WorkloadCacheData(
            server_name='nwpc_op',
            collected_time=datetime(2018, 9, 20, 9, 14, 0),
            update_time=datetime(2018, 9, 20, 9, 15, 0),
            status={
                'node': '/',
                'path': '/',
                'status': 'complete'
            }
        )

        data_dict = {
            'server_name': 'nwpc_op',
            'collected_time': datetime(2018, 9, 20, 9, 14, 0),
            'update_time': datetime(2018, 9, 20, 9, 15, 0),
            'status': {
                'node': '/',
                'path': '/',
                'status': 'complete'
            }
        }

        assert data.to_dict() == data_dict


class TestWorkloadCache(object):
    def test_construction(self):
        cache = WorkloadCache()

        cache = WorkloadCache(
            ticket_id=1,
            owner='my',
            repo='my_repo',
            timestamp=datetime(2018, 9, 20, 9, 17, 0),
            data=WorkloadCacheData(
                server_name='nwpc_op',
                collected_time=datetime(2018, 9, 20, 9, 14, 0),
                update_time=datetime(2018, 9, 20, 9, 15, 0),
                status={
                    'node': '/',
                    'path': '/',
                    'status': 'complete'
                }
            )
        )

    def test_to_json(self):
        cache = WorkloadCache(
            ticket_id=1,
            owner='my',
            repo='my_repo',
            timestamp=datetime(2018, 9, 20, 9, 17, 0),
            data=WorkloadCacheData(
                server_name='nwpc_op',
                collected_time=datetime(2018, 9, 20, 9, 14, 0),
                update_time=datetime(2018, 9, 20, 9, 15, 0),
                status={
                    'node': '/',
                    'path': '/',
                    'status': 'complete'
                }
            )
        )

        cache_dict = {
            'ticket_id': 1,
            'owner': 'my',
            'repo': 'my_repo',
            'timestamp': datetime(2018, 9, 20, 9, 17, 0),
            'data': {
                'server_name': 'nwpc_op',
                'collected_time': datetime(2018, 9, 20, 9, 14, 0),
                'update_time': datetime(2018, 9, 20, 9, 15, 0),
                'status': {
                    'node': '/',
                    'path': '/',
                    'status': 'complete'
                }
            }
        }

        assert cache.to_dict() == cache_dict
