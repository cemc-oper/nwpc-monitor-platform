"""
commit object

{
    id: id,
    owner: owner,
    repo: repo,
    timestamp: timestamp,
    data: {
        committer: committer name,
        type: commit type, [ status, task_check, ... ],
        tree_id: tree_id,
        committed_time: datetime
    }
}
"""
from .base import Base


class Commit(Base):
    def __init__(self):
        Base.__init__(self)

    def is_valid(self):
        if not Base.is_valid(self):
            return False
        return True

    def set_data(self, data):
        # check data
        if type(data) != dict:
            return False
        if 'committer' not in data:
            return False
        if 'type' not in data:
            return False

        # add data
        return Base.set_data(self, data)

    def to_dict(self):
        return Base.to_dict(self)

