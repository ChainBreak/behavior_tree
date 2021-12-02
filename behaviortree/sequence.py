from .node import Node

class Sequence(Node):

    def __init__(self, child_nodes=[]):
        super().__init__()
        self.child_nodes = child_nodes
        self.child_index = 0

    # def on_start(self):
    #     self.child_index = 0

    def on_tick(self):
        for child_node in self.child_nodes:

            active_behavior,status = child_node.tick()

            if status == "running":
                return active_behavior,"running"
            if status == "failure":
                return active_behavior,"failure"
        return active_behavior,"success"
        
        # # Prevent indexing outside child nodes array
        # max_index = len(self.child_nodes)-1
        # self.child_index = min(self.child_index, max_index)

        # # Select the current child index
        # child_node = self.child_nodes[self.child_index]

        # #Tick the child node
        # active_behavior,status = child_node.tick()

        # if status == "success":
        #     self.child_index += 1

        #     if self.child_index >= len(self.child_nodes):
        #         return active_behavior, "success"

        # if status == "failure":
        #     return active_behavior,"failure"

        # return active_behavior, "running"



        

  


