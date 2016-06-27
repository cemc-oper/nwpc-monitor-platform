"""
Base class of all objects using in nwpc_takler

{
    id: id,
    owner: owner,
    repo: repo,
    timestamp: datetime
}
"""
import datetime


class Base(object):
    def __init__(self):
        self.id = None
        self.owner = None
        self.repo = None
        self.timestamp = datetime.datetime.now()
        self.data = None

    def is_valid(self):
        if self.id is None:
            return False
        if self.owner is None:
            return False
        if self.repo is None:
            return False
        return True

    def set_data(self, data):
        self.data = data
        return True

    def to_dict(self):
        if not self.is_valid():
            return None

        result = {
            'id': self.id,
            'owner': self.owner,
            'repo': self.repo,
            'timestamp': self.timestamp,
            'data': self.data
        }
        return result
