from enum import Enum
from src.vectors import Vector3
from src import constants
from src.drone import DroneState

class FlightMode(Enum):
    IDLE = 'idle'
    TAKEOFF = 'takeoff'
    HOVER = 'hover'
    LANDING = 'landing'


class FlightController:
    def __init__(self, mass:float):
        self.mass = mass
        self.mode = FlightMode.IDLE
        self.schedule = []  # list of tuples (time, FlightMode)

    def add_phase(self, start_time:float, mode:FlightMode):
        self.schedule.append((start_time, mode))
        self.schedule.sort(key=lambda x: x[0])

    def update(self, current_time:float, drone_state:DroneState) -> Vector3:
        for i in range(len(self.schedule)):
            if self.schedule[i][0] > current_time:
                break
            self.mode = self.schedule[i][1]

        # apply state-based override
        if self.mode == FlightMode.LANDING and drone_state.position.z <= 0.0:
            self.mode = FlightMode.IDLE

        # update and return thrust
        return self._thrust_for_mode()

    
    def _thrust_for_mode(self) -> Vector3:
        # return the thrust mode based on self.mode
        if self.mode == FlightMode.IDLE:
            return Vector3(0, 0, 0)
        elif self.mode == FlightMode.TAKEOFF:
            return Vector3(0, 0, constants.TAKEOFF_THRUST)
        elif self.mode == FlightMode.HOVER:
            return Vector3(0, 0, constants.HOVER_THRUST)
        elif self.mode == FlightMode.LANDING:
            return Vector3(0, 0, constants.LANDING_THRUST)




