# coding: utf-8
from datetime import datetime

import pytest

from nmp_model.mongodb.commits.workload_commit import WorkloadCommitData, WorkloadCommit


class TestWorkloadCommitData(object):
    def test_construction(self):
        commit_data = WorkloadCommitData()

        commit_data = WorkloadCommitData(
            committer='committer',
            type='abnormal_jobs',
            tree_ticket_id=2,
            committed_time=datetime(2018, 9, 7, 16, 36, 0)
        )

        assert commit_data.committer == 'committer'

    def test_to_dict(self):
        commit_data = WorkloadCommitData(
            committer='committer',
            type='abnormal_jobs',
            tree_ticket_id=2,
            committed_time=datetime(2018, 9, 7, 16, 36, 0)
        )

        commit_data_dict = commit_data.to_dict()

        expected_commit_data_dict = {
            '_cls': 'WorkloadCommitData',
            'committer': 'committer',
            'type': 'abnormal_jobs',
            'tree_ticket_id': 2,
            'committed_time': datetime(2018, 9, 7, 16, 36, 0)
        }

        assert commit_data_dict == expected_commit_data_dict


class TestWorkloadCommit(object):
    def test_construction(self):
        commit = WorkloadCommit()

        commit = WorkloadCommit(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 7, 16, 36, 0),
            data=WorkloadCommitData(
                committer='committer',
                type='abnormal_jobs',
                tree_ticket_id=2,
                committed_time=datetime(2018, 9, 7, 16, 36, 0)
            )
        )

    def test_set_data(self):
        commit = WorkloadCommit(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 7, 16, 36, 0),
        )

        commit_data = WorkloadCommitData(
            committer='committer',
            type='abnormal_jobs',
            tree_ticket_id=2,
            committed_time=datetime(2018, 9, 7, 16, 36, 0)
        )

        commit.set_data(commit_data)

        data = {}
        with pytest.raises(TypeError):
            commit.set_data(data)

    def test_to_dict(self):
        commit = WorkloadCommit(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 7, 16, 36, 0),
            data=WorkloadCommitData(
                committer='committer',
                type='abnormal_jobs',
                tree_ticket_id=2,
                committed_time=datetime(2018, 9, 7, 16, 36, 0)
            )
        )

        commit_dict = {
            'ticket_id': 1,
            'owner': 'owner',
            'repo': 'repo',
            'timestamp': datetime(2018, 9, 7, 16, 36, 0),
            'data': {
                '_cls': 'WorkloadCommitData',
                'committer': 'committer',
                'type': 'abnormal_jobs',
                'tree_ticket_id': 2,
                'committed_time': datetime(2018, 9, 7, 16, 36, 0)
            }
        }

        assert commit.to_dict() == commit_dict
