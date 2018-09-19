# coding: utf-8
"""
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
    EmbeddedDocument, StringField, DictField, BooleanField, EmbeddedDocumentListField, \
    EmbeddedDocumentField, DateTimeField, ListField

from nmp_model.mongodb.blob import Blob, BlobData


class CheckResult(EmbeddedDocument):
    is_condition_fit = BooleanField()

    meta = {
        'allow_inheritance': True
    }

    def to_dict(self):
        return {
            'is_condition_fit': self.is_condition_fit,
        }


class StatusCheckResult(CheckResult):
    expected_value = DictField()
    value = StringField()

    def to_dict(self):
        result_dict = CheckResult.to_dict(self)
        result_dict.update({
            'expected_value': self.expected_value,
            'value': self.value
        })
        return result_dict


class VariableCheckResult(CheckResult):
    variable_name = StringField()
    expected_value = DictField()
    value = StringField()

    def to_dict(self):
        result_dict = CheckResult.to_dict(self)
        result_dict.update({
            'variable_name': self.variable_name,
            'expected_value': self.expected_value,
            'value': self.value
        })
        return result_dict


class UnfitNode(EmbeddedDocument):
    node_path = StringField()
    check_results = EmbeddedDocumentListField(CheckResult)

    def to_dict(self):
        return {
            'node_path': self.node_path,
            'check_results': [check_result.to_dict() for check_result in self.check_results]
        }


class UnfitNodesContent(EmbeddedDocument):
    name = StringField()
    trigger = ListField(DictField())
    check_time = DateTimeField()
    unfit_nodes = EmbeddedDocumentListField(UnfitNode)

    def to_dict(self):
        return {
            'name': self.name,
            'trigger': self.trigger,
            'check_time': self.check_time,
            'unfit_nodes': [unfit_node.to_dict() for unfit_node in self.unfit_nodes]
        }


class UnfitNodesBlobData(BlobData):
    name = StringField()
    content = EmbeddedDocumentField(UnfitNodesContent)

    def to_dict(self):
        return {
            'name': self.name,
            'content': self.content.to_dict()
        }


class UnfitNodesBlob(Blob):
    data = EmbeddedDocumentField(UnfitNodesBlobData)
