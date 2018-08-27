# coding: utf-8
from nwpc_workflow_model.visitor import NodeVisitor
from .node_status import NodeStatus


class ErrorStatusTaskVisitor(NodeVisitor):
    def __init__(self):
        NodeVisitor.__init__(self)
        self.level = 0
        self.error_task_list = []

    def visit(self, node):
        if node.status == NodeStatus.Aborted and node.is_leaf():
            self.error_task_list.append(node)

    def before_visit_child(self):
        self.level += 1

    def after_visit_child(self):
        self.level -= 1
