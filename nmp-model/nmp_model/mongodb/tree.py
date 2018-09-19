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
                    type: type, [ status, aborted_tasks ],
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
    type = StringField(choices=["status", "aborted_tasks", "unfit_tasks"])
    name = StringField()
    blob_ticket_id = IntField()

    def to_dict(self):
        result = {
            'type': self.type,
            'name': self.name,
            'blob_ticket_id': self.blob_ticket_id
        }
        return result


class TreeData(EmbeddedDocument):
    nodes = EmbeddedDocumentListField(TreeNode)

    meta = {
        'collection': 'trees'
    }

    def to_dict(self):
        return {
            'nodes': [node.to_dict() for node in self.nodes]
        }


class Tree(Base):
    data = TreeData()

    def set_data(self, data):
        if not isinstance(data, TreeData):
            raise TypeError("data must be TreeData")

        return Base.set_data(self, data)

    def to_dict(self):
        return Base.to_dict(self)