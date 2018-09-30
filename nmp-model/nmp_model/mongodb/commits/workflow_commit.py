# coding: utf-8
from mongoengine import StringField, EmbeddedDocumentField

from nmp_model.mongodb.commit import CommitData, Commit


class WorkflowCommitData(CommitData):
    type = StringField(choices=['status', 'task_check'])


class WorkflowCommit(Commit):
    data = EmbeddedDocumentField(WorkflowCommitData)
