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
from datetime import datetime
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField, StringField, IntField, DateTimeField

from .base import Base


class TreeNode(EmbeddedDocument):
    type = StringField(choices=["status", "aborted_tasks"])
    name = StringField()
    blob_id = IntField()

    def to_dict(self):
        result = {
            'type': self.type,
            'name': self.name,
            'blob_id': self.blob_id
        }
        return result


class TreeData(EmbeddedDocument):
    nodes = EmbeddedDocumentListField(TreeNode)

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