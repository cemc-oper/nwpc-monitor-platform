# coding: utf-8
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
from datetime import datetime
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, StringField, IntField, DateTimeField

from .base import Base


class CommitData(EmbeddedDocument):
    committer = StringField()
    type = StringField(choices=['status', 'task_check'])
    tree_id = IntField()
    committed_time = DateTimeField(default=datetime.utcnow())

    def to_dict(self):
        return {
            'committer': self.committer,
            'type': self.type,
            'tree_id': self.tree_id,
            'committed_time': self.committed_time
        }


class Commit(Base):
    data = EmbeddedDocumentField(CommitData)

    def is_valid(self):
        if not Base.is_valid(self):
            return False
        return True

    def set_data(self, data):
        if not isinstance(data, CommitData):
            raise TypeError("data must be CommitData")
        Base.set_data(self, data)

    def to_dict(self):
        return Base.to_dict(self)

