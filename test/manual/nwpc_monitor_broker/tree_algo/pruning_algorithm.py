import os
import json
import datetime

from nwpc_work_flow_model.sms.bunch import Bunch
from nwpc_work_flow_model.sms.visitor import \
    pre_order_travel_dict, pre_order_travel, NodeVisitor, ErrorStatusTaskVisitor


class NodeCountVisitor(NodeVisitor):
    def __init__(self):
        NodeVisitor.__init__(self)
        self.level = 0
        self.max_level = 0
        self.count = 0

    def visit(self, node):
        self.count += 1

    def before_visit_child(self):
        self.level += 1
        if self.max_level < self.level:
            self.max_level = self.level

    def after_visit_child(self):
        self.level -= 1


class PruningErrorStatusTaskVisitor(NodeVisitor):
    def __init__(self):
        NodeVisitor.__init__(self)
        self.level = 0
        self.error_task_list = []
        self.count = 0

    def visit(self, node):
        if node.status in ['que', 'act', 'com']:
            node.children = []
            return

        if node.status == 'abo' and node.is_leaf():
            self.error_task_list.append(node)
        self.count += 1

    def before_visit_child(self):
        self.level += 1

    def after_visit_child(self):
        self.level -= 1


def main():
    file_path = os.path.join(os.path.dirname(__file__) + "/../data/data_errors_78.json")
    with open(file_path, 'r') as f:
        data = json.load(f)
        status_dict = data["data"]["content"]["status"]
        visitor = NodeCountVisitor()
        pre_order_travel_dict(status_dict, visitor)
        print(visitor.max_level, visitor.count)

        tree = Bunch.create_from_dict(status_dict)
        start_time = datetime.datetime.now()
        error_visitor = ErrorStatusTaskVisitor()
        pre_order_travel(tree, error_visitor)
        end_time = datetime.datetime.now()
        print("error tasks: ", len(error_visitor.error_task_list))
        print(end_time - start_time)

        print("Pruning:")
        tree = Bunch.create_from_dict(status_dict)
        start_time = datetime.datetime.now()
        error_visitor = PruningErrorStatusTaskVisitor()
        pre_order_travel(tree, error_visitor)
        end_time = datetime.datetime.now()
        print("error tasks: ", len(error_visitor.error_task_list))
        print(end_time - start_time)
        print("visitor count: ", error_visitor.count)

        print("end")


if __name__ == "__main__":
    main()