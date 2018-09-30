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
        tree_ticket_id: tree_ticket_id,
        committed_time: datetime
    }
}
"""
from datetime import datetime
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, StringField, IntField, DateTimeField

from .base import Base


class CommitData(EmbeddedDocument):
    committer = StringField()
    tree_ticket_id = IntField()
    type = StringField()
    committed_time = DateTimeField(default=datetime.utcnow())

    meta = {
        'allow_inheritance': True,
    }

    def to_dict(self):
        return self.to_mongo().to_dict()


class Commit(Base):
    data = EmbeddedDocumentField(CommitData)

    meta = {
        'collection': 'commits',
        'allow_inheritance': True,
        'abstract': True
    }

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

