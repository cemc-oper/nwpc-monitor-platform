# coding: utf-8
from datetime import datetime

import pytest

from nmp_model.mongodb.commits.workflow_commit import WorkflowCommitData, WorkflowCommit


class TestWorkflowCommitData(object):
    def test_construction(self):
        commit_data = WorkflowCommitData()

        commit_data = WorkflowCommitData(
            committer='committer',
            type='status',
            tree_ticket_id=2,
            committed_time=datetime(2018, 9, 7, 16, 36, 0)
        )

        assert commit_data.committer == 'committer'

    def test_to_dict(self):
        commit_data = WorkflowCommitData(
            committer='committer',
            type='status',
            tree_ticket_id=2,
            committed_time=datetime(2018, 9, 7, 16, 36, 0)
        )

        commit_data_dict = commit_data.to_dict()

        expected_commit_data_dict = {
            '_cls': 'WorkflowCommitData',
            'committer': 'committer',
            'type': 'status',
            'tree_ticket_id': 2,
            'committed_time': datetime(2018, 9, 7, 16, 36, 0)
        }

        assert commit_data_dict == expected_commit_data_dict


class TestWorkflowCommit(object):
    def test_construction(self):
        commit = WorkflowCommit()

        commit = WorkflowCommit(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 7, 16, 36, 0),
            data=WorkflowCommitData(
                committer='committer',
                type='status',
                tree_ticket_id=2,
                committed_time=datetime(2018, 9, 7, 16, 36, 0)
            )
        )

    def test_set_data(self):
        commit = WorkflowCommit(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 7, 16, 36, 0),
        )

        commit_data = WorkflowCommitData(
            committer='committer',
            type='status',
            tree_ticket_id=2,
            committed_time=datetime(2018, 9, 7, 16, 36, 0)
        )

        commit.set_data(commit_data)

        data = {}
        with pytest.raises(TypeError):
            commit.set_data(data)

    def test_to_dict(self):
        commit = WorkflowCommit(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 7, 16, 36, 0),
            data=WorkflowCommitData(
                committer='committer',
                type='status',
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
                '_cls': 'WorkflowCommitData',
                'committer': 'committer',
                'type': 'status',
                'tree_ticket_id': 2,
                'committed_time': datetime(2018, 9, 7, 16, 36, 0)
            }
        }

        assert commit.to_dict() == commit_dict
