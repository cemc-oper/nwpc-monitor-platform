import os
import json

from nwpc_work_flow_model.sms.visitor import pre_order_travel_dict, NodeVisitor


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


def main():
    file_path = os.path.join(os.path.dirname(__file__) + "/../data/data_eps_nwpc_qu.json")
    with open(file_path, 'r') as f:
        data = json.load(f)
        status_dict = data["data"]["content"]["status"]
        visitor = NodeCountVisitor()
        pre_order_travel_dict(status_dict, visitor)
        print(visitor.max_level, visitor.count)
        print("end")


if __name__ == "__main__":
    main()