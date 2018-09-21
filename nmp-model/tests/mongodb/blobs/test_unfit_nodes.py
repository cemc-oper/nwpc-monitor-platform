# coding: utf-8
from datetime import datetime
from mongoengine import connect

from nmp_model.mongodb.blobs.unfit_nodes import \
    StatusCheckResult, VariableCheckResult, UnfitNode, UnfitNodesContent, UnfitNodesBlobData, UnfitNodesBlob


class TestUnfitNodesContent(object):
    def test_construct(self):
        content = UnfitNodesContent()

        content = UnfitNodesContent(
            name="meso post 00H",
            trigger=[
                {
                    'type': 'time',
                    'time': '03:31:00',
                }
            ],
            check_time=datetime(2018, 9, 19, 15, 7, 0),
            unfit_nodes=[
                UnfitNode(
                    node_path='/f1/t1',
                    check_results=[
                        StatusCheckResult(
                            is_condition_fit=True,
                            expected_value={
                                'operator': 'in',
                                'fields': ['completed', 'submitted']
                            },
                            value='completed'
                        ),
                        VariableCheckResult(
                            is_condition_fit=False,
                            expected_value={
                                'type': 'date',
                                'operator': 'equal',
                                'fields': 'current'
                            },
                            value='20180907'
                        )
                    ]
                )
            ]
        )

        assert len(content.unfit_nodes) == 1

    def test_to_dict(self):
        content = UnfitNodesContent(
            name="meso post 00H",
            trigger=[
                {
                    'type': 'time',
                    'time': '03:31:00',
                }
            ],
            check_time=datetime(2018, 9, 19, 15, 7, 0),
            unfit_nodes=[
                UnfitNode(
                    node_path='/f1/t1',
                    check_results=[
                        StatusCheckResult(
                            is_condition_fit=True,
                            expected_value={
                                'operator': 'in',
                                'fields': ['completed', 'submitted']
                            },
                            value='completed'
                        ),
                        VariableCheckResult(
                            is_condition_fit=False,
                            variable_name='SMSDATE',
                            expected_value={
                                'type': 'date',
                                'operator': 'equal',
                                'fields': 'current'
                            },
                            value='20180907'
                        )
                    ]
                )
            ]
        )

        content_dict = {
            'name': "meso post 00H",
            'trigger': [
                {
                    'type': 'time',
                    'time': '03:31:00',
                }
            ],
            'check_time': datetime(2018, 9, 19, 15, 7, 0),
            'unfit_nodes': [
                {
                    'node_path': '/f1/t1',
                    'check_results': [
                        {
                            'is_condition_fit': True,
                            'expected_value': {
                                'operator': 'in',
                                'fields': ['completed', 'submitted']
                            },
                            'value': 'completed'
                        },
                        {
                            'is_condition_fit': False,
                            'variable_name': 'SMSDATE',
                            'expected_value': {
                                'type': 'date',
                                'operator': 'equal',
                                'fields': 'current'
                            },
                            'value': '20180907'
                        }
                    ]
                }
            ]
        }
        assert content.to_dict() == content_dict


class TestUnfitNodeBlob(object):
    def test_construct(self):
        blob = UnfitNodesBlob()

        blob_data = UnfitNodesBlobData(
            name='sms_check_task_unfit_nodes',
            content=UnfitNodesContent(
                name="meso post 00H",
                trigger=[
                    {
                        'type': 'time',
                        'time': '03:31:00',
                    }
                ],
                check_time=datetime(2018, 9, 19, 15, 7, 0),
                unfit_nodes=[
                    UnfitNode(
                        node_path='/f1/t1',
                        check_results=[
                            StatusCheckResult(
                                is_condition_fit=True,
                                expected_value={
                                    'operator': 'in',
                                    'fields': ['completed', 'submitted']
                                },
                                value='completed'
                            ),
                            VariableCheckResult(
                                is_condition_fit=False,
                                variable_name='SMSDATE',
                                expected_value={
                                    'type': 'date',
                                    'operator': 'equal',
                                    'fields': 'current'
                                },
                                value='20180907'
                            )
                        ]
                    )
                ]
            )

        )

        blob = UnfitNodesBlob(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0),
            data=blob_data
        )

        assert blob.ticket_id == 1

    def test_save(self):
        blob_data = UnfitNodesBlobData(
            name='sms_check_task_unfit_nodes',
            content=UnfitNodesContent(
                name="meso post 00H",
                trigger=[
                    {
                        'type': 'time',
                        'time': '03:31:00',
                    }
                ],
                check_time=datetime(2018, 9, 19, 15, 7, 0),
                unfit_nodes=[
                    UnfitNode(
                        node_path='/f1/t1',
                        check_results=[
                            StatusCheckResult(
                                is_condition_fit=True,
                                expected_value={
                                    'operator': 'in',
                                    'fields': ['completed', 'submitted']
                                },
                                value='completed'
                            ),
                            VariableCheckResult(
                                is_condition_fit=False,
                                variable_name='SMSDATE',
                                expected_value='20180906',
                                value='20180907'
                            )
                        ]
                    )
                ]
            )

        )

        blob = UnfitNodesBlob(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 5, 11, 29, 0),
            data=blob_data
        )

        connect('mongoenginetest', host='mongomock://localhost')
        blob.save()

        query_objects = UnfitNodesBlob.objects(__raw__={'data._cls': 'UnfitNodesBlobData'}).all()
        assert len(query_objects) == 1
