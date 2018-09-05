# coding: utf-8
from mongoengine import \
    EmbeddedDocument, StringField, GenericEmbeddedDocumentField, \
    DateTimeField, DictField, IntField, BooleanField, \
    ListField, EmbeddedDocumentListField


from nmp_model.mongodb.blob import Blob, BlobData


class StatusContent(EmbeddedDocument):
    collected_time = DateTimeField()
    update_time = DateTimeField()
    status = DictField()

    def to_dict(self):
        return {
            'collected_time': self.collected_time,
            'update_time': self.update_time,
            'status': self.status
        }


class StatusBlobData(BlobData):
    content = StatusContent()


class StatusBlob(Blob):
    data = StatusBlobData()
