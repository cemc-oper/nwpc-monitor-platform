"""
blob object

{
    id: id,
    owner: owner,
    repo: repo,
    timestamp: timestamp,
    data: {
        type: type, [ status, aborted_tasks, unfit_nodes ]
        name: name
        content: {
            defined by type
        }
    }
}

type: status
content:
{
    collected_time: time,
    update_time: time,
    status: status dict

}

type: aborted_tasks
content:
{
    status_blob_id: blob id of status object,
    tasks: array of task status
    [
        {
            path: node path,
            name: node name,
            status: node status
        }
    ]

}

type: unfit_nodes
content:
{
    unfit_node_list: array of unfit tasks
    [
        {
            node_path: node path,
            check_list_result: array of unfit check results
                check result:
                common fields
                {
                    type: [status, variable],
                    is_condition_fit: False,
                    value: object
                }
                
                type status:
                    value: {
                        expected_value: {
                            operator: in
                            fields: [submitted, active, complete]
                        },
                        value: value
                    }
                
                type variable:
                    value: { 
                        expected_value: 20170523,
                        value: 20170523
                    }
        }
    ]
}
"""
from mongoengine import \
    EmbeddedDocument, StringField, GenericEmbeddedDocumentField

from .base import Base


class BlobData(EmbeddedDocument):
    type = StringField(default=None)
    name = StringField(default=None)
    content = GenericEmbeddedDocumentField(default=None)

    meta = {
        'allow_inheritance': True,
    }

    def to_dict(self):
        if self.content is None:
            content_dict = None
        else:
            content_dict = self.content.to_dict()
        return {
            'type': self.type,
            'name': self.name,
            'content': content_dict
        }


class Blob(Base):
    data = BlobData()

    meta = {
        'allow_inheritance': True,
        'collection': 'blobs'
    }

    def set_data(self, data):
        if not isinstance(data, BlobData):
            raise TypeError("Blob's data must be BlobData.")
        Base.set_data(self, data)

    def to_dict(self):
        object_dict = Base.to_dict(self)
        data_dict = self.data.to_dict()
        object_dict['data'] = data_dict

        return object_dict
