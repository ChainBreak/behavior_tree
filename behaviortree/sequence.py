from .node import Node

class Sequence(Node):

    def __init__(self, child_nodes=[]):
        self.child_nodes = child_nodes


    def __call__(self):
        for child_node in self.child_nodes:

            node,status = child_node()

            if status == "running":
                return node,"running"
            if status == "failure":
                return node,"failure"
        return node,"success"

  


