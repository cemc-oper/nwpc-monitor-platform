# coding: utf-8
from mongoengine import StringField, EmbeddedDocumentField

from nmp_model.mongodb.commit import CommitData, Commit


class WorkloadCommitData(CommitData):
    type = StringField(choices=['jobs', 'abnormal_jobs', 'queue_info'])


class WorkloadCommit(Commit):
    data = EmbeddedDocumentField(WorkloadCommitData)
