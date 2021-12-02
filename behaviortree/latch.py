from .node import Node

class Latch(Node):

    def __init__(self, child_node):
        super().__init__()
        self.child_nodes.append(child_node)

        self.latch = False

    def on_start(self):
        self.latch = False

    def on_tick(self):

        if self.latch:
            return None, "success"

        active_behavior, status = self.child_nodes[0].tick()

        if status == "success":
            self.latch = True

        return active_behavior, status


