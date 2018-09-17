# coding: utf-8
from datetime import datetime

import pytest

from nmp_model.mongodb.commit import CommitData, Commit


class TestCommitData(object):
    def test_construction(self):
        commit_data = CommitData()

        commit_data = CommitData(
            committer='committer',
            type='status',
            tree_id=2,
            committed_time=datetime(2018, 9, 7, 16, 36, 0)
        )

        assert commit_data.committer == 'committer'

    def test_to_dict(self):
        commit_data = CommitData(
            committer='committer',
            type='status',
            tree_id=2,
            committed_time=datetime(2018, 9, 7, 16, 36, 0)
        )

        commit_data_dict = {
            'committer': 'committer',
            'type': 'status',
            'tree_id': 2,
            'committed_time': datetime(2018, 9, 7, 16, 36, 0)
        }

        assert commit_data.to_dict() == commit_data_dict


class TestCommit(object):
    def test_construction(self):
        commit = Commit()

        commit = Commit(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 7, 16, 36, 0),
            data=CommitData(
                committer='committer',
                type='status',
                tree_id=2,
                committed_time=datetime(2018, 9, 7, 16, 36, 0)
            )
        )

    def test_set_data(self):
        commit = Commit(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 7, 16, 36, 0),
        )

        commit_data = CommitData(
            committer='committer',
            type='status',
            tree_id=2,
            committed_time=datetime(2018, 9, 7, 16, 36, 0)
        )

        commit.set_data(commit_data)

        data = {}
        with pytest.raises(TypeError):
            commit.set_data(data)

    def test_to_dict(self):
        commit = Commit(
            ticket_id=1,
            owner='owner',
            repo='repo',
            timestamp=datetime(2018, 9, 7, 16, 36, 0),
            data=CommitData(
                committer='committer',
                type='status',
                tree_id=2,
                committed_time=datetime(2018, 9, 7, 16, 36, 0)
            )
        )

        commit_dict = {
            'ticket_id': 1,
            'owner': 'owner',
            'repo': 'repo',
            'timestamp': datetime(2018, 9, 7, 16, 36, 0),
            'data': {
                'committer': 'committer',
                'type': 'status',
                'tree_id': 2,
                'committed_time': datetime(2018, 9, 7, 16, 36, 0)
            }
        }

        assert commit.to_dict() == commit_dict
