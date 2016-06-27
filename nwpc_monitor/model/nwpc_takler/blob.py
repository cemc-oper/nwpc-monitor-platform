"""
blob object

{
    id: id,
    owner: owner,
    repo: repo,
    timestamp: timestamp,
    data: {
        type: type, [ status, aborted_tasks ]
        name: name
        content: {
            defined by type
        }
    }
}

type: status
content:
{
    collected_time: time,
    update_time: time,
    status: status dict

}

type: aborted_tasks
content:
{
    status_blob_id: blob id of status object,
    tasks: array of task status
    [
        {
            path: node path,
            name: node name,
            status: node status
        }
    ]

}
"""
from .base import Base


class Blob(Base):
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
        if 'type' not in data:
            return False
        if 'name' not in data:
            return False
        if 'content' not in data:
            return False

        # add data
        return Base.set_data(self, data)

    def to_dict(self):
        return Base.to_dict(self)