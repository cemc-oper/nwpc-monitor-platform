# coding: utf-8
from mongoengine import StringField

from nmp_model.mongodb.tree import TreeNode


class WorkloadTreeNode(TreeNode):
    type = StringField(choices=["jobs", "abnormal_jobs", "queue_info"])
