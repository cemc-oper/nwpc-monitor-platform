# coding: utf-8
"""
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
from mongoengine import \
    EmbeddedDocument, StringField, IntField, EmbeddedDocumentListField, EmbeddedDocumentField

from nmp_model.mongodb.blob import Blob, BlobData


class TaskStatusField(EmbeddedDocument):
    path = StringField()
    name = StringField()
    status = StringField()

    def to_dict(self):
        return {
            'path': self.path,
            'name': self.name,
            'status': self.status
        }


class AbortedTasksContent(EmbeddedDocument):
    status_blob_id = IntField()
    tasks = EmbeddedDocumentListField(TaskStatusField)

    def to_dict(self):
        return {
            'status_blob_id': self.status_blob_id,
            'tasks': [task.to_dict() for task in self.tasks]
        }


class AbortedTasksBlobData(BlobData):
    content = EmbeddedDocumentField(AbortedTasksContent)


class AbortedTasksBlob(Blob):
    data = EmbeddedDocumentField(AbortedTasksBlobData)
