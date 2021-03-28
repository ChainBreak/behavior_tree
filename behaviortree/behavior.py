
class Behavior():

    def __init__(self):
        self.status = "failure"

    def __call__(self):
        self.status = self.tick()

        if self.status == None:
            self.status = "running"
            
        return self,self.status

    def tick(self):
        raise NotImplementedError()