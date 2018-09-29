# coding: utf-8
import datetime

from mongoengine import StringField, DictField, DateTimeField, EmbeddedDocumentField, EmbeddedDocument
from nmp_model.mongodb.base import Base


class WorkflowCacheData(EmbeddedDocument):
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


class WorkflowCache(Base):
    data = EmbeddedDocumentField(WorkflowCacheData)

    meta = {
        'allow_inheritance': True,
        'collection': 'workload_caches'
    }
