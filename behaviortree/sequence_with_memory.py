from .node import Node

class SequenceWithMemory(Node):

    def __init__(self, child_nodes=[]):
        super().__init__()
        self.child_nodes = child_nodes
        self.child_index = 0

    def on_start(self):
        self.child_index = 0

    def on_tick(self):
        
        num_child_nodes = len(self.child_nodes)

        for self.child_index in range(self.child_index, num_child_nodes):

            child_node = self.child_nodes[self.child_index]

            active_behavior,status = child_node.tick()

            if status == "success":
                continue

            if status == "running":
                return active_behavior, "running"

            if status == "failure":
                return active_behavior, "failure"

        return active_behavior, "success"



        

  


