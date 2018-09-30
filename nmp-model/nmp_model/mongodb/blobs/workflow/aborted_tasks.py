# coding: utf-8
"""
type: aborted_tasks
content:
{
    status_blob_ticket_id: blob id of status object,
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
import datetime
from mongoengine import \
    EmbeddedDocument, StringField, IntField, ListField, DictField, EmbeddedDocumentField, DateTimeField

from nmp_model.mongodb.blob import Blob, BlobData


class AbortedTasksContent(EmbeddedDocument):
    status_blob_ticket_id = IntField()
    server_name = StringField()
    collected_time = DateTimeField()
    tasks = ListField(DictField())

    def to_dict(self):
        return {
            'status_blob_ticket_id': self.status_blob_ticket_id,
            'server_name': self.server_name,
            'collected_time': self.collected_time,
            'tasks': self.tasks
        }


class AbortedTasksBlobData(BlobData):
    content = EmbeddedDocumentField(AbortedTasksContent)


class AbortedTasksBlob(Blob):
    data = EmbeddedDocumentField(AbortedTasksBlobData)
