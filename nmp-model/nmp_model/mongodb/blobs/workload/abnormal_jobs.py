# coding: utf-8
import datetime
from mongoengine import \
    EmbeddedDocument, StringField, IntField, ListField, DictField, EmbeddedDocumentField, DateTimeField

from nmp_model.mongodb.blob import Blob, BlobData


class AbnormalJobsContent(EmbeddedDocument):
    plugins = ListField(DictField())
    abnormal_jobs = ListField(DictField())

    def to_dict(self):
        return self.to_mongo().to_dict()


class AbnormalJobsBlobData(BlobData):
    workload_system = StringField(choices=['loadleveler', 'slurm'])
    user_name = StringField()
    collected_time = DateTimeField()
    update_time = DateTimeField(default=datetime.datetime.utcnow)
    content = EmbeddedDocumentField(AbnormalJobsContent)

    def to_dict(self):
        return self.to_mongo().to_dict()


class AbnormalJobsBlob(Blob):
    data = EmbeddedDocumentField(AbnormalJobsBlobData)
