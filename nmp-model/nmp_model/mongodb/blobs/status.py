# coding: utf-8
"""
type: status
content:
{
    collected_time: time,
    update_time: time,
    status: status dict

}
"""

from mongoengine import \
    EmbeddedDocument, DateTimeField, DictField, EmbeddedDocumentField, StringField

from nmp_model.mongodb.blob import Blob, BlobData


class StatusContent(EmbeddedDocument):
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


class StatusBlobData(BlobData):
    type = StringField(default='StatusBlobData')
    content = EmbeddedDocumentField(StatusContent)


class StatusBlob(Blob):
    data = EmbeddedDocumentField(StatusBlobData)
