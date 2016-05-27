from .node import Node

class Bunch(Node):
    def __init__(self):
        Node.__init__(self)
        self.parent = None
        self.children = list()
        self.name = ''
        self.status = 'unknown'

    def add_node_status(self, node_status_object):

        node_path = node_status_object['path']
        node_status = node_status_object['status']
        node_name = node_status_object['name']

        if node_path == '/':
            self.status = node_status
            return self

        node = None
        if node_path[0] != '/':
            return node

        node_path = node_path[1:]
        tokens = node_path.split("/")
        cur_node = self
        for a_token in tokens:
            t_node = None
            for a_child in cur_node.children:
                if a_child.name == a_token:
                    t_node = a_child
                    break
            if t_node is None:
                t_node = Node()
                t_node.parent = cur_node
                t_node.name = node_name
                t_node.status = node_status
                t_node.children = list()
                cur_node.add_child(t_node)
            cur_node = t_node
        return cur_node