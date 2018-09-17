"""
ref object

{
    id: id,
    owner: owner,
    repo: repo,
    timestamp: timestamp,
    data: {
        key: key,
        type: type, [ commit, tree, blob ]
        id: id
    }
}
"""
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, StringField, IntField

from .base import Base


class RefData(EmbeddedDocument):
    key = StringField()
    type = StringField(choices=['commit', 'tree', 'blob'])
    id = IntField()

    def to_dict(self):
        return {
            'key': self.key,
            'type': self.type,
            'id': self.id
        }


class Ref(Base):
    data = EmbeddedDocumentField(RefData)

    def set_data(self, data):
        if not isinstance(data, RefData):
            raise TypeError("data must be RefData")

        return Base.set_data(self, data)

    def to_dict(self):
        return Base.to_dict(self)
