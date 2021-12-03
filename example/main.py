import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import time
import math

from behaviortree import Sequence, Selector, Latch, SequenceWithMemory
from behaviors import FuelCheck, RunEngine, StopEngine, Refill, PowerDemandCheck, FuelLow
class GeneratorController():

    def __init__(self):
        self.state={
            "engine_running": False,
            "engine_stopped": True,
            "engine_speed" : 0.0,
            "key_position": "off",
            "fuel_level"   : 100,
            "fuel_needed"   : False,
            "power_demand": 0,
            "crank_time"  : 0.0,
            "crank_flag"  : False,
            "refill_flag" : False,

        }
        self.last_t = time.time()

        self.behavior_tree = self.create_behavior_tree()

    def create_behavior_tree(self):

        return Selector([
            self.refill_engine_if_fuel_low(),
            self.run_engine_if_demand_high(),
            StopEngine(self.state),
        ])

    
    def refill_engine_if_fuel_low(self):
        return SequenceWithMemory([
            FuelLow(self.state),
            StopEngine(self.state),
            Refill(self.state),
        ])

    def run_engine_if_demand_high(self):
        return Sequence([
            PowerDemandCheck(self.state,30),
            RunEngine(self.state),
        ])



    def __call__(self):
        self.tick()

    def tick(self):
        node,status = self.behavior_tree.tick()
        self.behavior_tree.check_if_ticked()
        print(type(node),status)
        self.print_state()
        self.simulate_generator()

    def print_state(self):
        print()
        for key,value in self.state.items():
            print(f"{key:15}: {value}")


    def simulate_generator(self):
        t = time.time()
        dt = t-self.last_t
        self.last_t = t

        #Simulate power demand as a sin wave
        self.state["power_demand"] = 50 + 50*math.sin(2 * math.pi * t/30)

        #Simulate fuel usage 5% per second
        self.state["fuel_level"] -= self.state["engine_running"] * 5 * dt

        #Simulate fuel refil 20% per second
        self.state["fuel_level"] += self.state["refill_flag"] * 20 * dt

        # Clamp the level in the fuel tank between 0-100
        self.state["fuel_level"] = max(0,min(100,self.state["fuel_level"]))
        
        # Count how long the engine has been cranking
        if self.state["crank_flag"]:
            self.state["crank_time"] += dt
        else:
            self.state["crank_time"] = 0

        # Logic for ramping the engine up or down
        if (self.state["engine_running"] or self.state["crank_flag"]) and self.state["fuel_level"] > 1 and self.state["key_position"] == "on":
            self.state["engine_speed"] += 50*dt
        else:
            self.state["engine_speed"] -= 50*dt

        # Clamp the engine speed between 0-100
        self.state["engine_speed"] = max(0,min(100,self.state["engine_speed"]))

        # Logic for if the engine is running
        self.state["engine_running"] = self.state["engine_speed"] > 90

        # Logic for if engine is stopped
        self.state["engine_stopped"] = self.state["engine_speed"] < 10

        # Reset flags
        self.state["crank_flag"] = False
        self.state["refill_flag"] = False


if __name__ == "__main__":
    controller = GeneratorController()
 
    while True:
        controller()
        time.sleep(0.1)
        

        
        

