# coding: utf-8
import datetime

from mongoengine import StringField, DictField, DateTimeField, EmbeddedDocumentField, EmbeddedDocument
from .base import Base


class WorkloadCacheData(EmbeddedDocument):
    server_name = StringField()
    collected_time = DateTimeField()
    update_time = DateTimeField()
    status = DictField()

    def to_dict(self):
        return {
            'server_name': self.server_name,
            'collected_time': self.collected_time,
            'update_time': self.update_time,
            'status': self.status
        }


class WorkloadCache(Base):
    data = EmbeddedDocumentField(WorkloadCacheData)

    meta = {
        'allow_inheritance': True,
        'collection': 'workload_caches'
    }
