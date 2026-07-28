from src.drone import Drone
from src.physics import PhysicsEngine
from src.flight_controller import FlightController
from src import constants
import csv
from pathlib import Path

class Simulation:
    def __init__(self, drone: Drone, flight_controller: FlightController, dt=constants.DEFAULT_DT):
        self.drone = drone
        self.dt = dt
        self.engine = PhysicsEngine()
        self.time = 0.0
        self.history = []
        self.flight_controller = flight_controller

    def step(self):
        # 0 compute and set thrust
        thrust = self.flight_controller.update(self.time)
        self.drone.set_thrust(thrust)

        # 1 compute net force
        net_force = self.engine.compute_net_force(self.drone.thrust, self.drone.mass, self.drone.state.velocity)
        
        # 2 calculate acceleration
        acceleration = self.engine.compute_acceleration(net_force, self.drone.mass)

        # 2 set acceleration to drone
        self.drone.set_acceleration(acceleration)

        # 3 update drone state
        self.drone.update(self.dt)

        # 4 advance time by dt
        self.time += self.dt

        # 5 record history
        self.log_state(net_force)
        
    def run(self, duration:float):
        while round(self.time,4) < duration:
            self.step()

        return self.history


    def log_state(self, net_force:Vector3):
        self.history.append({"time":self.time, "position":self.drone.state.position, "velocity":self.drone.state.velocity, "acceleration":self.drone.state.acceleration, 'net_force':net_force, 'drone_mode':self.flight_controller.mode})


    def export_csv(self, filepath:str):
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            # write the header row
            writer.writerow(['time', 'position_x', 'position_y', 'position_z', 'velocity_x', 'velocity_y', 'velocity_z', 'acceleration_x', 'acceleration_y', 'acceleration_z', 'net_force_x', 'net_force_y', 'net_force_z', 'drone_mode'])
            # write one new row per history entry
            for entry in self.history:
                writer.writerow([entry['time'], entry['position'].x, entry['position'].y, entry['position'].z, entry['velocity'].x, entry['velocity'].y, entry['velocity'].z, entry['acceleration'].x, entry['acceleration'].y, entry['acceleration'].z, entry['net_force'].x, entry['net_force'].y, entry['net_force'].z, entry['drone_mode'].value])

    
        