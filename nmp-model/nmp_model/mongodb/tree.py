"""
tree object

{
    id: id,
    owner: owner,
    repo: repo,
    timestamp: timestamp,
    data: {
        nodes: array of blob
            [
                {
                    type: type, [ status, aborted_tasks ],
                    name: name,
                    blob_id: id
                }
            ]
    }
}
"""
from .base import Base


class TreeNode(object):
    def __init__(self):
        self.type = None
        self.name = None
        self.blob_id = None

    def to_dict(self):
        result = {
            'type': self.type,
            'name': self.name,
            'blob_id': self.blob_id
        }
        return result


class Tree(Base):
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
        if 'nodes' not in data:
            return False

        # add data
        return Base.set_data(self, data)

    def to_dict(self):
        return Base.to_dict(self)