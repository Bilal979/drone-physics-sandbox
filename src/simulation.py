from src.drone import Drone
from src.physics import PhysicsEngine
from src import constants

class Simulation:
    def __init__(self, drone: Drone, dt=constants.DEFAULT_DT):
        self.drone = drone
        self.dt = dt
        self.engine = PhysicsEngine()
        self.time = 0.0
        self.history = []

    def step(self):
        # 1 compute net force
        net_force = self.engine.compute_net_force(self.drone.thrust, self.drone.mass)

        # 2 apply force to drone
        self.drone.apply_force(net_force)

        # 3 update drone state
        self.drone.update(self.dt)

        # 4 advance time by dt
        self.time += self.dt

        # 5 record history
        self.log_state()
        
    def run(self, duration:float):
        while round(self.time,4) < duration:
            self.step()

        return self.history


    def log_state(self):
        self.history.append({"time":f'{self.time}', "position":self.drone.state.position, "velocity":self.drone.state.velocity, "acceleration":self.drone.state.acceleration})


