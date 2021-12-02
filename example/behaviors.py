import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))


from behaviortree import Behavior


class EngineBehavior(Behavior):
    def __init__(self,state):
        super().__init__()
        self.state = state


class FuelCheck(EngineBehavior):
    def on_tick(self):
        if self.state["fuel_needed"]:
            return "failure"
        return "success"

class FuelLow(EngineBehavior):
    def on_tick(self):
        if self.state["fuel_level"] < 5:
            return "success"
        return "failure"

class RunEngine(EngineBehavior):
    def on_tick(self):
        self.state["key_position"] = "on"
        
        if not self.state["engine_running"]:
            self.state["crank_flag"]   = True

        if self.state["crank_time"] > 10:
            return "failure"

        return "running"

class StopEngine(EngineBehavior):
    def on_tick(self):
        self.state["key_position"] = "off"

        if self.state["engine_stopped"]:
            return "success"

        return "running"

class Refill(EngineBehavior):
    def on_tick(self):
        self.state["refill_flag"] = True
        if self.state["fuel_level"] > 99:
            return "success"
        return "running"

class PowerDemandCheck(Behavior):
    def __init__(self,state,demand_threshold):
        super().__init__()
        self.state = state
        self.demand_threshold = demand_threshold

    def on_tick(self):
        if self.state["power_demand"] > self.demand_threshold:
            return "success"
        else:
            return "failure"
