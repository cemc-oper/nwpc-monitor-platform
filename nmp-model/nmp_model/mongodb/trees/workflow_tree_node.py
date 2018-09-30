# coding: utf-8
from mongoengine import StringField

from nmp_model.mongodb.tree import TreeNode


class WorkflowTreeNode(TreeNode):
    type = StringField(choices=["status", "aborted_tasks", "unfit_tasks"])
