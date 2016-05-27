"""
Node:

    status:
        first three characters of the status word.
        unk: unknown
        sus: suspended
        com: complete
        que: queued
        sub: submitted
        act: active
        abo: aborted
        shu: shutdown
        hal: halted
"""

class Node(object):
    def __int__(self):
        self.parent = None
        self.children = list()
        self.name = ''
        self.status = 'unk'

    """
    node:
        {
            "name": "node",
            "type": "record",
            "fields": [
                {"name": "name", "type": "string"},
                {"name": "status", "type": "string"},
                {"name": "path", "type": "string"},
                {
                    "name": "children",
                    "type": "array",
                    "items": {"type":"node"}
                }
            ]
        }
    """
    def to_dict(self):
        ret = dict()
        ret['name'] = self.name
        ret['children'] = list()
        ret['status'] = self.status
        ret['path'] = self.get_node_path()
        for a_child in self.children:
            ret['children'].append(a_child.to_dict())
        return ret

    @staticmethod
    def create_from_dict(node_dict, parent=None):
        # use parent is evil.
        node = Node()
        node.parent = parent
        node.name = node_dict['name']
        node.status = node_dict['status']
        node.children = []
        for a_child_item in node_dict['children']:
            a_child_node = Node.create_from_dict(a_child_item, parent=node)
            node.children.append(a_child_node)
        return node

    def add_child(self, node):
        self.children.append(node)

    def get_node_path(self):
        cur_node = self
        node_list = []
        while cur_node is not None:
            node_list.insert(0, cur_node.name)
            cur_node = cur_node.parent
        node_path = "/".join(node_list)
        if node_path == "":
            node_path = "/"
        return node_path

    def is_suite(self):
        if self.parent:
            parent = self.parent
            if parent.parent is None:
                return True
        return False

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            # check whether child is an alias
            alias_flag = False
            for a_child in self.children:
                if a_child.is_alias():
                    alias_flag = True
                    break
            if alias_flag:
                return True
            else:
                return False

    def is_alias(self):
        if len(self.children) != 0:
            return False

        if self.name.startswith('alias'):
            return True

        return False