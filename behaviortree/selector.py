from .node import Node

class Selector(Node):

    def __init__(self, child_nodes=[]):
        super().__init__()
        
        self.child_nodes = child_nodes

    def on_tick(self):

        for child_node in self.child_nodes:

            active_behavior, status = child_node.tick()

            if status == "success":
                return active_behavior,"success"

            if status == "running":
                return active_behavior,"running"
            
            if status == "failure":
                continue

        return active_behavior, "failure"


