"""
Base class of all objects using in nwpc_takler

{
    id: id,
    owner: owner,
    repo: repo,
    timestamp: datetime
}
"""
import datetime

from mongoengine import Document, \
    StringField, DateTimeField, GenericEmbeddedDocumentField, IntField, EmbeddedDocument


class Base(Document):
    ticket_id = IntField(default=None)
    owner = StringField(default=None)
    repo = StringField(default=None)
    timestamp = DateTimeField(required=True, default=datetime.datetime.utcnow)
    data = GenericEmbeddedDocumentField(default=None)

    meta = {
        'allow_inheritance': True,
        'abstract': True
    }

    def set_data(self, data):
        if not isinstance(data, EmbeddedDocument):
            raise TypeError("data must be EmbeddedDocument.")
        self.data = data

    def is_valid(self):
        if self.ticket_id is None:
            return False
        if self.owner is None:
            return False
        if self.repo is None:
            return False
        return True

    def to_dict(self):
        if not self.is_valid():
            return None

        if self.data is None:
            data_dict = None
        elif hasattr(self.data, 'to_dict'):
            data_dict = self.data.to_dict()
        else:
            try:
                data_dict = dict(self.data)
            except ValueError as e:
                data_dict = self.data

        result = {
            'ticket_id': self.ticket_id,
            'owner': self.owner,
            'repo': self.repo,
            'timestamp': self.timestamp,
            'data': data_dict
        }
        return result
