# coding: utf-8
from mongoengine import \
    EmbeddedDocument, StringField, IntField, EmbeddedDocumentListField, EmbeddedDocumentField

from nmp_model.mongodb.blob import Blob, BlobData


class TaskStatusField(EmbeddedDocument):
    path = StringField()
    name = StringField()
    status = StringField()


class AbortedTasksContent(EmbeddedDocument):
    status_blot_id = IntField()
    tasks = EmbeddedDocumentListField(TaskStatusField)


class AbortedTasksBlobData(BlobData):
    content = EmbeddedDocumentField(AbortedTasksContent)


class AbortedTasksBlob(Blob):
    data = EmbeddedDocumentField(AbortedTasksBlobData)
