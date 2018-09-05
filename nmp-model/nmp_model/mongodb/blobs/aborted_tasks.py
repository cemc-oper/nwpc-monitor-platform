# coding: utf-8
from mongoengine import \
    EmbeddedDocument, StringField, GenericEmbeddedDocumentField, \
    DateTimeField, DictField, IntField, BooleanField, \
    ListField, EmbeddedDocumentListField


class TaskStatusField(EmbeddedDocument):
    path = StringField()
    name = StringField()
    status = StringField()


class AbortedTasksContent(EmbeddedDocument):
    status_blot_id = IntField()
    tasks = EmbeddedDocumentListField(TaskStatusField)