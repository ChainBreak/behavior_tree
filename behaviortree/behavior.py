from .node import Node

class Behavior(Node):

    def tick(self):

        self.ticked = True 

        # If we just became active
        if not self.active:
            self.active = True
            self.on_start()

        self.status = self.on_tick()

        if self.status == None:
            self.status = "running"

        if self.status == "success" or self.status == "failure":
            self.active = False
            self.on_end()

        return self, self.status

