# coding: utf-8
from mongoengine import \
    EmbeddedDocument, StringField, DictField, BooleanField, EmbeddedDocumentListField, EmbeddedDocumentField

from nmp_model.mongodb.blob import Blob, BlobData


class CheckValue(EmbeddedDocument):
    meta = {
        'allow_inheritance': True,
    }


class StatusCheckValue(CheckValue):
    expected_value = DictField()
    value = StringField()


class VariableCheckValue(CheckValue):
    expected_value = StringField()
    value = StringField()


class CheckResult(EmbeddedDocument):
    type = StringField()
    is_condition_fit = BooleanField()
    value = EmbeddedDocumentListField(CheckValue)


class UnfitNode(EmbeddedDocument):
    node_path = StringField()
    check_list_result = EmbeddedDocumentListField(CheckResult)


class UnfitNodesContent(EmbeddedDocument):
    unfit_node_list = EmbeddedDocumentListField(UnfitNode)


class UnfitNodesBlobData(BlobData):
    content = EmbeddedDocumentField(UnfitNodesContent)


class UnfitNodesBlob(Blob):
    data = EmbeddedDocumentField(UnfitNodesBlobData)
