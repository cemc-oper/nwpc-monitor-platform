# coding: utf-8
import datetime

from mongoengine import (
    StringField, DictField, DateTimeField, EmbeddedDocumentField, EmbeddedDocument, ListField,
    GenericEmbeddedDocumentField)
from nmp_model.mongodb.base import Base


class JobListContent(EmbeddedDocument):
    items = ListField(DictField())


class QueueInfoListContent(EmbeddedDocument):
    items = ListField(DictField())


class WorkloadCacheData(EmbeddedDocument):
    workload_system = StringField(choices=['loadleveler', 'slurm'])
    user_name = StringField()
    collected_time = DateTimeField()
    update_time = DateTimeField(default=datetime.datetime.utcnow)
    request = DictField()
    content = GenericEmbeddedDocumentField(choices=[JobListContent, QueueInfoListContent])


class WorkloadCache(Base):
    data = EmbeddedDocumentField(WorkloadCacheData)

    meta = {
        'allow_inheritance': True,
        'collection': 'workload_caches'
    }
