# coding: utf-8
from datetime import datetime

from nmp_model.mongodb.cache.workload_cache import (
    JobListContent, QueueInfoListContent, WorkloadCacheData, WorkloadCache)


class TestWorkloadCacheData(object):
    def test_construction(self):
        empty_data = WorkloadCacheData()

        job_list_data = WorkloadCacheData(
            workload_system='loadleveler',
            user_name='nwp_qu',
            collected_time=datetime(2018, 9, 20, 9, 14, 0),
            update_time=datetime(2018, 9, 20, 9, 15, 0),
            request={
                'app': 'nwpc_hpc_collector.loadleveler.status',
                'type': 'command',
                'command': {
                    'program': 'loadleveler_status',
                    'sub_command': 'collect'
                }
            },
            content=JobListContent(
                items=[
                    {
                        "props": [
                            {
                                "text": "cmb20n04.6543838.0",
                                "value": "cmb20n04.6543838.0",
                                "data": "cmb20n04.6543838.0",
                                "id": "llq.id"
                            },
                            {
                                "text": "wmc_qu1",
                                "value": "wmc_qu1",
                                "data": "wmc_qu1",
                                "id": "llq.owner"
                            },
                            {
                                "text": "operation1",
                                "value": "operation1",
                                "data": "operation1",
                                "id": "llq.class"
                            },
                            {
                                "text": "/cma/g5/wmc_qu1/WRF/CPEFS/WSWC/arwpost-s.cmd",
                                "value": "/cma/g5/wmc_qu1/WRF/CPEFS/WSWC/arwpost-s.cmd",
                                "data": "/cma/g5/wmc_qu1/WRF/CPEFS/WSWC/arwpost-s.cmd",
                                "id": "llq.job_script"
                            },
                            {
                                "text": "R",
                                "value": "Running",
                                "data": "R",
                                "id": "llq.status"
                            },
                            {
                                "text": "09/04 00:42",
                                "value": "Tue Sep  4 00:42:55 2018",
                                "data": "2018-09-04 00:42:55",
                                "id": "llq.queue_date"
                            },
                            {
                                "text": "50",
                                "value": "50",
                                "data": 50.0,
                                "id": "llq.priority"
                            }
                        ]
                    },
                    {
                        "items": [
                            {
                                "text": "cmb20n04.6543838.0",
                                "value": "cmb20n04.6543838.0",
                                "data": "cmb20n04.6543838.0",
                                "id": "llq.id"
                            },
                            {
                                "text": "wmc_qu1",
                                "value": "wmc_qu1",
                                "data": "wmc_qu1",
                                "id": "llq.owner"
                            },
                            {
                                "text": "operation1",
                                "value": "operation1",
                                "data": "operation1",
                                "id": "llq.class"
                            },
                            {
                                "text": "/cma/g5/wmc_qu1/WRF/CPEFS/WSWC/arwpost-s.cmd",
                                "value": "/cma/g5/wmc_qu1/WRF/CPEFS/WSWC/arwpost-s.cmd",
                                "data": "/cma/g5/wmc_qu1/WRF/CPEFS/WSWC/arwpost-s.cmd",
                                "id": "llq.job_script"
                            },
                            {
                                "text": "R",
                                "value": "Running",
                                "data": "R",
                                "id": "llq.status"
                            },
                            {
                                "text": "09/04 00:42",
                                "value": "Tue Sep  4 00:42:55 2018",
                                "data": "2018-09-04 00:42:55",
                                "id": "llq.queue_date"
                            },
                            {
                                "text": "50",
                                "value": "50",
                                "data": 50.0,
                                "id": "llq.priority"
                            }
                        ]
                    }
                ]
            )
        )

        queue_info_data = WorkloadCacheData(
            workload_system='loadleveler',
            user_name='nwp_qu',
            collected_time=datetime(2018, 9, 20, 9, 14, 0),
            update_time=datetime(2018, 9, 20, 9, 15, 0),
            request={
                'app': 'nwpc_hpc_collector.loadleveler.info',
                'type': 'command',
                'command': {
                    'program': 'loadleveler_info',
                    'sub_command': 'collect'
                }
            },
            content=QueueInfoListContent(
                items=[
                    {
                        'props': [
                            {
                                'text': 'largemem',
                                'value': 'largemem',
                                'data': 'largemem',
                                'id': 'llclass.name'
                            },
                            {
                                'text': '1792',
                                'value': '1792',
                                'data': 1792.0,
                                'id': 'llclass.free_slots'
                            },
                            {
                                'text': '1952',
                                'value': '1952',
                                'data': 1952.0,
                                'id': 'llclass.maximum_slots'
                            }
                        ]
                    },
                    {
                        'props': [
                            {
                                'text': 'operation2',
                                'value': 'operation2',
                                'data': 'operation2',
                                'id': 'llclass.name'
                            },
                            {
                                'text': '224',
                                'value': '224',
                                'data': 224.0,
                                'id': 'llclass.free_slots'
                            },
                            {
                                'text': '224',
                                'value': '224',
                                'data': 224.0,
                                'id': 'llclass.maximum_slots'
                            }
                        ]
                    },
                ]
            )
        )

    def test_to_dict(self):
        data = WorkloadCacheData(
            workload_system='loadleveler',
            user_name='nwp_qu',
            collected_time=datetime(2018, 9, 20, 9, 14, 0),
            update_time=datetime(2018, 9, 20, 9, 15, 0),
            request={
                'app': 'nwpc_hpc_collector.loadleveler.info',
                'type': 'command',
                'command': {
                    'program': 'loadleveler_info',
                    'sub_command': 'collect'
                }
            },
            content=QueueInfoListContent(
                items=[
                    {
                        'props': [
                            {
                                'text': 'largemem',
                                'value': 'largemem',
                                'data': 'largemem',
                                'id': 'llclass.name'
                            },
                            {
                                'text': '1792',
                                'value': '1792',
                                'data': 1792.0,
                                'id': 'llclass.free_slots'
                            },
                            {
                                'text': '1952',
                                'value': '1952',
                                'data': 1952.0,
                                'id': 'llclass.maximum_slots'
                            }
                        ]
                    },
                    {
                        'props': [
                            {
                                'text': 'operation2',
                                'value': 'operation2',
                                'data': 'operation2',
                                'id': 'llclass.name'
                            },
                            {
                                'text': '224',
                                'value': '224',
                                'data': 224.0,
                                'id': 'llclass.free_slots'
                            },
                            {
                                'text': '224',
                                'value': '224',
                                'data': 224.0,
                                'id': 'llclass.maximum_slots'
                            }
                        ]
                    },
                ]
            )
        )

        data_dict = data.to_mongo().to_dict()

        expected_data_dict = {
            'workload_system': 'loadleveler',
            'user_name': 'nwp_qu',
            'collected_time': datetime(2018, 9, 20, 9, 14, 0),
            'update_time': datetime(2018, 9, 20, 9, 15, 0),
            'request': {
                'app': 'nwpc_hpc_collector.loadleveler.info',
                'type': 'command',
                'command': {
                    'program': 'loadleveler_info',
                    'sub_command': 'collect'
                }
            },
            'content': {
                '_cls': 'QueueInfoListContent',
                'items': [
                    {
                        'props': [
                            {
                                'text': 'largemem',
                                'value': 'largemem',
                                'data': 'largemem',
                                'id': 'llclass.name'
                            },
                            {
                                'text': '1792',
                                'value': '1792',
                                'data': 1792.0,
                                'id': 'llclass.free_slots'
                            },
                            {
                                'text': '1952',
                                'value': '1952',
                                'data': 1952.0,
                                'id': 'llclass.maximum_slots'
                            }
                        ]
                    },
                    {
                        'props': [
                            {
                                'text': 'operation2',
                                'value': 'operation2',
                                'data': 'operation2',
                                'id': 'llclass.name'
                            },
                            {
                                'text': '224',
                                'value': '224',
                                'data': 224.0,
                                'id': 'llclass.free_slots'
                            },
                            {
                                'text': '224',
                                'value': '224',
                                'data': 224.0,
                                'id': 'llclass.maximum_slots'
                            }
                        ]
                    },
                ]
            }
        }

        assert data_dict == expected_data_dict


class TestWorkloadCache(object):
    def test_construction(self):
        cache = WorkloadCache()

        cache = WorkloadCache(
            ticket_id=1,
            owner='nwp_xp',
            repo='aix_nwp_xp',
            timestamp=datetime(2018, 9, 20, 9, 17, 0),
            data=WorkloadCacheData(
                workload_system='loadleveler',
                user_name='nwp_qu',
                collected_time=datetime(2018, 9, 20, 9, 14, 0),
                update_time=datetime(2018, 9, 20, 9, 15, 0),
                request={
                    'app': 'nwpc_hpc_collector.loadleveler.info',
                    'type': 'command',
                    'command': {
                        'program': 'loadleveler_info',
                        'sub_command': 'collect'
                    }
                },
                content=QueueInfoListContent(
                    items=[
                        {
                            'props': [
                                {
                                    'text': 'largemem',
                                    'value': 'largemem',
                                    'data': 'largemem',
                                    'id': 'llclass.name'
                                },
                                {
                                    'text': '1792',
                                    'value': '1792',
                                    'data': 1792.0,
                                    'id': 'llclass.free_slots'
                                },
                                {
                                    'text': '1952',
                                    'value': '1952',
                                    'data': 1952.0,
                                    'id': 'llclass.maximum_slots'
                                }
                            ]
                        },
                        {
                            'props': [
                                {
                                    'text': 'operation2',
                                    'value': 'operation2',
                                    'data': 'operation2',
                                    'id': 'llclass.name'
                                },
                                {
                                    'text': '224',
                                    'value': '224',
                                    'data': 224.0,
                                    'id': 'llclass.free_slots'
                                },
                                {
                                    'text': '224',
                                    'value': '224',
                                    'data': 224.0,
                                    'id': 'llclass.maximum_slots'
                                }
                            ]
                        },
                    ]
                )
            )
        )

    def test_to_dict(self):
        cache = WorkloadCache(
            ticket_id=1,
            owner='nwp_xp',
            repo='aix_nwp_xp',
            timestamp=datetime(2018, 9, 20, 9, 17, 0),
            data=WorkloadCacheData(
                workload_system='loadleveler',
                user_name='nwp_qu',
                collected_time=datetime(2018, 9, 20, 9, 14, 0),
                update_time=datetime(2018, 9, 20, 9, 15, 0),
                request={
                    'app': 'nwpc_hpc_collector.loadleveler.info',
                    'type': 'command',
                    'command': {
                        'program': 'loadleveler_info',
                        'sub_command': 'collect'
                    }
                },
                content=QueueInfoListContent(
                    items=[
                        {
                            'props': [
                                {
                                    'text': 'largemem',
                                    'value': 'largemem',
                                    'data': 'largemem',
                                    'id': 'llclass.name'
                                },
                                {
                                    'text': '1792',
                                    'value': '1792',
                                    'data': 1792.0,
                                    'id': 'llclass.free_slots'
                                },
                                {
                                    'text': '1952',
                                    'value': '1952',
                                    'data': 1952.0,
                                    'id': 'llclass.maximum_slots'
                                }
                            ]
                        },
                        {
                            'props': [
                                {
                                    'text': 'operation2',
                                    'value': 'operation2',
                                    'data': 'operation2',
                                    'id': 'llclass.name'
                                },
                                {
                                    'text': '224',
                                    'value': '224',
                                    'data': 224.0,
                                    'id': 'llclass.free_slots'
                                },
                                {
                                    'text': '224',
                                    'value': '224',
                                    'data': 224.0,
                                    'id': 'llclass.maximum_slots'
                                }
                            ]
                        },
                    ]
                )
            )
        )
        cache_dict = cache.to_mongo().to_dict()

        expected_cache_dict = {
            '_cls': 'WorkloadCache',
            'ticket_id': 1,
            'owner': 'nwp_xp',
            'repo': 'aix_nwp_xp',
            'timestamp': datetime(2018, 9, 20, 9, 17, 0),
            'data': {
                'workload_system': 'loadleveler',
                'user_name': 'nwp_qu',
                'collected_time': datetime(2018, 9, 20, 9, 14, 0),
                'update_time': datetime(2018, 9, 20, 9, 15, 0),
                'request': {
                    'app': 'nwpc_hpc_collector.loadleveler.info',
                    'type': 'command',
                    'command': {
                        'program': 'loadleveler_info',
                        'sub_command': 'collect'
                    }
                },
                'content': {
                    '_cls': 'QueueInfoListContent',
                    'items': [
                        {
                            'props': [
                                {
                                    'text': 'largemem',
                                    'value': 'largemem',
                                    'data': 'largemem',
                                    'id': 'llclass.name'
                                },
                                {
                                    'text': '1792',
                                    'value': '1792',
                                    'data': 1792.0,
                                    'id': 'llclass.free_slots'
                                },
                                {
                                    'text': '1952',
                                    'value': '1952',
                                    'data': 1952.0,
                                    'id': 'llclass.maximum_slots'
                                }
                            ]
                        },
                        {
                            'props': [
                                {
                                    'text': 'operation2',
                                    'value': 'operation2',
                                    'data': 'operation2',
                                    'id': 'llclass.name'
                                },
                                {
                                    'text': '224',
                                    'value': '224',
                                    'data': 224.0,
                                    'id': 'llclass.free_slots'
                                },
                                {
                                    'text': '224',
                                    'value': '224',
                                    'data': 224.0,
                                    'id': 'llclass.maximum_slots'
                                }
                            ]
                        },
                    ]
                }
            }
        }

        assert cache_dict == expected_cache_dict
