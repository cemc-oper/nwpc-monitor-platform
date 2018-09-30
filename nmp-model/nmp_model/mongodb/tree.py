# coding: utf-8
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
                    type: type,
                    name: name,
                    blob_ticket_id: id
                }
            ]
    }
}
"""
from mongoengine import EmbeddedDocument, EmbeddedDocumentListField, StringField, IntField

from .base import Base


class TreeNode(EmbeddedDocument):
    type = StringField()
    name = StringField()
    blob_ticket_id = IntField()

    meta = {
        'allow_inheritance': True,
    }

    def to_dict(self):
        return self.to_mongo().to_dict()


class TreeData(EmbeddedDocument):
    nodes = EmbeddedDocumentListField(TreeNode)

    meta = {
        'collection': 'trees'
    }

    def to_dict(self):
        return self.to_mongo().to_dict()


class Tree(Base):
    data = TreeData()

    def set_data(self, data):
        if not isinstance(data, TreeData):
            raise TypeError("data must be TreeData")

        return Base.set_data(self, data)

    def to_dict(self):
        return Base.to_dict(self)