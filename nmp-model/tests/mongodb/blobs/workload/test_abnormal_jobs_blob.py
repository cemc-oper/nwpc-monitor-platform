# coding: utf-8
from datetime import datetime
from mongoengine import connect

from nmp_model.mongodb.blobs.workload.abnormal_jobs import (
    AbnormalJobsBlob, AbnormalJobsBlobData, AbnormalJobsContent
)


class TestAbnormalJobsContent(object):
    def test_construct(self):
        content = AbnormalJobsContent()

        content = AbnormalJobsContent(
            plugins=[
                {
                    'name': 'warn_long_time_operation_job'
                }
            ],
            abnormal_jobs=[
                {
                    "props": [
                        {
                            "text": "cma19n02.5610339.0",
                            "value": "cma19n02.5610339.0",
                            "id": "llq.id",
                            "data": "cma19n02.5610339.0"
                        },
                        {
                            "text": "nwp_qu",
                            "value": "nwp_qu",
                            "id": "llq.owner",
                            "data": "nwp_qu"
                        },
                        {
                            "text": "normal1",
                            "value": "normal1",
                            "id": "llq.class",
                            "data": "normal1"
                        },
                        {
                            "text": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm",
                            "value": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm",
                            "id": "llq.job_script",
                            "data": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm"
                        },
                        {
                            "text": "R",
                            "value": "Running",
                            "id": "llq.status",
                            "data": "R"
                        },
                        {
                            "text": "06/01 10:34",
                            "value": "Thu Jun  1 10:34:08 2017",
                            "id": "llq.queue_date",
                            "data": "2017-06-01 10:34:08"
                        },
                        {
                            "text": "100",
                            "value": "100",
                            "id": "llq.priority",
                            "data": 100.0
                        }
                    ]
                },
                {
                    "props": [
                        {
                            "text": "cma19n02.5610338.0",
                            "value": "cma19n02.5610338.0",
                            "id": "llq.id",
                            "data": "cma19n02.5610338.0"
                        },
                        {
                            "text": "nwp_qu",
                            "value": "nwp_qu",
                            "id": "llq.owner",
                            "data": "nwp_qu"
                        },
                        {
                            "text": "normal1",
                            "value": "normal1",
                            "id": "llq.class",
                            "data": "normal1"
                        },
                        {
                            "text": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm",
                            "value": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm",
                            "id": "llq.job_script",
                            "data": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm"
                        },
                        {
                            "text": "R",
                            "value": "Running",
                            "id": "llq.status",
                            "data": "R"
                        },
                        {
                            "text": "06/01 10:34",
                            "value": "Thu Jun  1 10:34:05 2017",
                            "id": "llq.queue_date",
                            "data": "2017-06-01 10:34:05"
                        },
                        {
                            "text": "100",
                            "value": "100",
                            "id": "llq.priority",
                            "data": 100.0
                        }
                    ]
                },
            ]
        )
        assert len(content.abnormal_jobs) == 2

    def test_to_dict(self):
        content = AbnormalJobsContent(
            plugins=[
                {
                    'name': 'warn_long_time_operation_job'
                }
            ],
            abnormal_jobs=[
                {
                    "props": [
                        {
                            "text": "cma19n02.5610339.0",
                            "value": "cma19n02.5610339.0",
                            "id": "llq.id",
                            "data": "cma19n02.5610339.0"
                        },
                        {
                            "text": "nwp_qu",
                            "value": "nwp_qu",
                            "id": "llq.owner",
                            "data": "nwp_qu"
                        },
                        {
                            "text": "normal1",
                            "value": "normal1",
                            "id": "llq.class",
                            "data": "normal1"
                        },
                        {
                            "text": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm",
                            "value": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm",
                            "id": "llq.job_script",
                            "data": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm"
                        },
                        {
                            "text": "R",
                            "value": "Running",
                            "id": "llq.status",
                            "data": "R"
                        },
                        {
                            "text": "06/01 10:34",
                            "value": "Thu Jun  1 10:34:08 2017",
                            "id": "llq.queue_date",
                            "data": "2017-06-01 10:34:08"
                        },
                        {
                            "text": "100",
                            "value": "100",
                            "id": "llq.priority",
                            "data": 100.0
                        }
                    ]
                },
                {
                    "props": [
                        {
                            "text": "cma19n02.5610338.0",
                            "value": "cma19n02.5610338.0",
                            "id": "llq.id",
                            "data": "cma19n02.5610338.0"
                        },
                        {
                            "text": "nwp_qu",
                            "value": "nwp_qu",
                            "id": "llq.owner",
                            "data": "nwp_qu"
                        },
                        {
                            "text": "normal1",
                            "value": "normal1",
                            "id": "llq.class",
                            "data": "normal1"
                        },
                        {
                            "text": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm",
                            "value": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm",
                            "id": "llq.job_script",
                            "data": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm"
                        },
                        {
                            "text": "R",
                            "value": "Running",
                            "id": "llq.status",
                            "data": "R"
                        },
                        {
                            "text": "06/01 10:34",
                            "value": "Thu Jun  1 10:34:05 2017",
                            "id": "llq.queue_date",
                            "data": "2017-06-01 10:34:05"
                        },
                        {
                            "text": "100",
                            "value": "100",
                            "id": "llq.priority",
                            "data": 100.0
                        }
                    ]
                },
            ]
        )

        content_dict = content.to_dict()

        expected_content_dict = {
            'plugins': [
                {
                    'name': 'warn_long_time_operation_job'
                }
            ],
            'abnormal_jobs': [
                {
                    "props": [
                        {
                            "text": "cma19n02.5610339.0",
                            "value": "cma19n02.5610339.0",
                            "id": "llq.id",
                            "data": "cma19n02.5610339.0"
                        },
                        {
                            "text": "nwp_qu",
                            "value": "nwp_qu",
                            "id": "llq.owner",
                            "data": "nwp_qu"
                        },
                        {
                            "text": "normal1",
                            "value": "normal1",
                            "id": "llq.class",
                            "data": "normal1"
                        },
                        {
                            "text": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm",
                            "value": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm",
                            "id": "llq.job_script",
                            "data": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm"
                        },
                        {
                            "text": "R",
                            "value": "Running",
                            "id": "llq.status",
                            "data": "R"
                        },
                        {
                            "text": "06/01 10:34",
                            "value": "Thu Jun  1 10:34:08 2017",
                            "id": "llq.queue_date",
                            "data": "2017-06-01 10:34:08"
                        },
                        {
                            "text": "100",
                            "value": "100",
                            "id": "llq.priority",
                            "data": 100.0
                        }
                    ]
                },
                {
                    "props": [
                        {
                            "text": "cma19n02.5610338.0",
                            "value": "cma19n02.5610338.0",
                            "id": "llq.id",
                            "data": "cma19n02.5610338.0"
                        },
                        {
                            "text": "nwp_qu",
                            "value": "nwp_qu",
                            "id": "llq.owner",
                            "data": "nwp_qu"
                        },
                        {
                            "text": "normal1",
                            "value": "normal1",
                            "id": "llq.class",
                            "data": "normal1"
                        },
                        {
                            "text": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm",
                            "value": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm",
                            "id": "llq.job_script",
                            "data": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm"
                        },
                        {
                            "text": "R",
                            "value": "Running",
                            "id": "llq.status",
                            "data": "R"
                        },
                        {
                            "text": "06/01 10:34",
                            "value": "Thu Jun  1 10:34:05 2017",
                            "id": "llq.queue_date",
                            "data": "2017-06-01 10:34:05"
                        },
                        {
                            "text": "100",
                            "value": "100",
                            "id": "llq.priority",
                            "data": 100.0
                        }
                    ]
                },
            ]
        }

        assert content_dict == expected_content_dict


class TestAbnormalJobsBlob(object):

    def test_construct(self):
        blob = AbnormalJobsBlob()

        blob_data = AbnormalJobsBlobData(
            workload_system='loadleveler',
            user_name='nwp_xp',
            collected_time=datetime(2018, 9, 30, 13, 28, 0),
            update_time=datetime(2018, 9, 30, 13, 28, 3),
            content=AbnormalJobsContent(
                plugins=[
                    {
                        'name': 'warn_long_time_operation_job'
                    }
                ],
                abnormal_jobs=[
                    {
                        "props": [
                            {
                                "text": "cma19n02.5610339.0",
                                "value": "cma19n02.5610339.0",
                                "id": "llq.id",
                                "data": "cma19n02.5610339.0"
                            },
                            {
                                "text": "nwp_qu",
                                "value": "nwp_qu",
                                "id": "llq.owner",
                                "data": "nwp_qu"
                            },
                            {
                                "text": "normal1",
                                "value": "normal1",
                                "id": "llq.class",
                                "data": "normal1"
                            },
                            {
                                "text": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm",
                                "value": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm",
                                "id": "llq.job_script",
                                "data": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm"
                            },
                            {
                                "text": "R",
                                "value": "Running",
                                "id": "llq.status",
                                "data": "R"
                            },
                            {
                                "text": "06/01 10:34",
                                "value": "Thu Jun  1 10:34:08 2017",
                                "id": "llq.queue_date",
                                "data": "2017-06-01 10:34:08"
                            },
                            {
                                "text": "100",
                                "value": "100",
                                "id": "llq.priority",
                                "data": 100.0
                            }
                        ]
                    },
                    {
                        "props": [
                            {
                                "text": "cma19n02.5610338.0",
                                "value": "cma19n02.5610338.0",
                                "id": "llq.id",
                                "data": "cma19n02.5610338.0"
                            },
                            {
                                "text": "nwp_qu",
                                "value": "nwp_qu",
                                "id": "llq.owner",
                                "data": "nwp_qu"
                            },
                            {
                                "text": "normal1",
                                "value": "normal1",
                                "id": "llq.class",
                                "data": "normal1"
                            },
                            {
                                "text": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm",
                                "value": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm",
                                "id": "llq.job_script",
                                "data": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm"
                            },
                            {
                                "text": "R",
                                "value": "Running",
                                "id": "llq.status",
                                "data": "R"
                            },
                            {
                                "text": "06/01 10:34",
                                "value": "Thu Jun  1 10:34:05 2017",
                                "id": "llq.queue_date",
                                "data": "2017-06-01 10:34:05"
                            },
                            {
                                "text": "100",
                                "value": "100",
                                "id": "llq.priority",
                                "data": 100.0
                            }
                        ]
                    },
                ]
            )
        )

        blob = AbnormalJobsBlob(
            ticket_id=1,
            owner='nwp_xp',
            repo='aix_nwp_xp',
            timestamp=datetime(2018, 9, 30, 13, 29, 0),
            data=blob_data
        )

        assert blob.ticket_id == 1

    def test_save(self):
        blob_data = AbnormalJobsBlobData(
            workload_system='loadleveler',
            user_name='nwp_xp',
            collected_time=datetime(2018, 9, 30, 13, 28, 0),
            update_time=datetime(2018, 9, 30, 13, 28, 3),
            content=AbnormalJobsContent(
                plugins=[
                    {
                        'name': 'warn_long_time_operation_job'
                    }
                ],
                abnormal_jobs=[
                    {
                        "props": [
                            {
                                "text": "cma19n02.5610339.0",
                                "value": "cma19n02.5610339.0",
                                "id": "llq.id",
                                "data": "cma19n02.5610339.0"
                            },
                            {
                                "text": "nwp_qu",
                                "value": "nwp_qu",
                                "id": "llq.owner",
                                "data": "nwp_qu"
                            },
                            {
                                "text": "normal1",
                                "value": "normal1",
                                "id": "llq.class",
                                "data": "normal1"
                            },
                            {
                                "text": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm",
                                "value": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm",
                                "id": "llq.job_script",
                                "data": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm"
                            },
                            {
                                "text": "R",
                                "value": "Running",
                                "id": "llq.status",
                                "data": "R"
                            },
                            {
                                "text": "06/01 10:34",
                                "value": "Thu Jun  1 10:34:08 2017",
                                "id": "llq.queue_date",
                                "data": "2017-06-01 10:34:08"
                            },
                            {
                                "text": "100",
                                "value": "100",
                                "id": "llq.priority",
                                "data": 100.0
                            }
                        ]
                    },
                    {
                        "props": [
                            {
                                "text": "cma19n02.5610338.0",
                                "value": "cma19n02.5610338.0",
                                "id": "llq.id",
                                "data": "cma19n02.5610338.0"
                            },
                            {
                                "text": "nwp_qu",
                                "value": "nwp_qu",
                                "id": "llq.owner",
                                "data": "nwp_qu"
                            },
                            {
                                "text": "normal1",
                                "value": "normal1",
                                "id": "llq.class",
                                "data": "normal1"
                            },
                            {
                                "text": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm",
                                "value": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm",
                                "id": "llq.job_script",
                                "data": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm"
                            },
                            {
                                "text": "R",
                                "value": "Running",
                                "id": "llq.status",
                                "data": "R"
                            },
                            {
                                "text": "06/01 10:34",
                                "value": "Thu Jun  1 10:34:05 2017",
                                "id": "llq.queue_date",
                                "data": "2017-06-01 10:34:05"
                            },
                            {
                                "text": "100",
                                "value": "100",
                                "id": "llq.priority",
                                "data": 100.0
                            }
                        ]
                    },
                ]
            )
        )

        blob = AbnormalJobsBlob(
            ticket_id=1,
            owner='nwp_xp',
            repo='aix_nwp_xp',
            timestamp=datetime(2018, 9, 30, 13, 29, 0),
            data=blob_data
        )

        connect('mongoenginetest', host='mongomock://localhost')
        blob.save()

        query_objects = AbnormalJobsBlob.objects(__raw__={'_cls': 'Blob.AbnormalJobsBlob'}).all()
        assert len(query_objects) == 1
