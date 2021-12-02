
class Node():

    def __init__(self):
        self.child_nodes = []
        self.status = "failure"
        self.active = False 
        self.ticked = False
  

    def tick(self):

        self.ticked = True 

        # If we just became active
        if not self.active:
            self.active = True
            self.on_start()

        active_behavior, self.status = self.on_tick()

        if self.status == None:
            self.status = "running"

        if self.status == "success" or self.status == "failure":
            self.active = False
            self.on_end()

        return active_behavior, self.status


    def check_if_ticked():

        if self.active and not self.ticked:
            self.active = False
            self.on_end()

        self.ticked = False

        for child_node in self.child_nodes:
            child_node.check_if_ticked()


    def on_start(self):
        pass

    def on_tick(self):
        raise NotImplementedError()

    def on_end(self):
        pass