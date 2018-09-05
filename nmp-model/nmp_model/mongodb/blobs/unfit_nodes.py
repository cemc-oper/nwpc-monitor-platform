# coding: utf-8
from mongoengine import \
    EmbeddedDocument, StringField, GenericEmbeddedDocumentField, \
    DateTimeField, DictField, IntField, BooleanField, \
    ListField, EmbeddedDocumentListField


class UnfitNodeField(EmbeddedDocument):
    type = StringField()
    is_condition_fit = BooleanField()
    value = GenericEmbeddedDocumentField()


class UnfitNodesContent(EmbeddedDocument):
    unfit_node_list = EmbeddedDocumentListField