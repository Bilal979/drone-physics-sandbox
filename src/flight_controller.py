from enum import Enum
from src.vectors import Vector3
from src import constants
from src.drone import DroneState
from src.waypoint_navigator import WaypointNavigator

class FlightMode(Enum):
    IDLE = 'idle'
    TAKEOFF = 'takeoff'
    HOVER = 'hover'
    LANDING = 'landing'
    NAVIGATE = 'navigate'


class FlightController:
    def __init__(self, mass:float, navigator:WaypointNavigator=None):
        self.mass = mass
        self.navigator = navigator
        self.mode = FlightMode.IDLE
        self.schedule = []  # list of tuples (time, FlightMode)
        self.hover_target = None

    def add_phase(self, start_time:float, mode:FlightMode):
        self.schedule.append((start_time, mode))
        self.schedule.sort(key=lambda x: x[0])

    def update(self, current_time:float, drone_state:DroneState) -> Vector3:
        for i in range(len(self.schedule)):
            if self.schedule[i][0] > current_time:
                break
            self.mode = self.schedule[i][1]

        # record hover target when entering hover mode
        if self.mode == FlightMode.HOVER and self.hover_target is None:
            self.hover_target = Vector3(drone_state.position.x, drone_state.position.y, drone_state.position.z)

        # reset hover target when leaving hover mode
        if self.mode != FlightMode.HOVER:
            self.hover_target = None

        # apply navigator thrust overide
        if self.mode == FlightMode.NAVIGATE and self.navigator is not None:
            if self.navigator.completed:
                self.mode = FlightMode.LANDING
            else:
                thrust = self.navigator.update(drone_state)
                return thrust

        # apply state-based override
        if self.mode == FlightMode.LANDING and drone_state.position.z <= 0.0:
            self.mode = FlightMode.IDLE

        # update and return thrust
        return self._thrust_for_mode(drone_state)

    
    def _thrust_for_mode(self, drone_state:DroneState) -> Vector3:
        # return the thrust mode based on self.mode
        if self.mode == FlightMode.IDLE:
            return Vector3(0, 0, 0)
        elif self.mode == FlightMode.TAKEOFF:
            return Vector3(0, 0, constants.TAKEOFF_THRUST)
        elif self.mode == FlightMode.HOVER:
            if self.hover_target is None:
                return Vector3(0, 0, constants.HOVER_THRUST)
            position_error = self.hover_target - drone_state.position
            position_force = position_error * constants.KP
            velocity_force = drone_state.velocity * constants.KD
            return position_force - velocity_force
        elif self.mode == FlightMode.LANDING:
            return Vector3(0, 0, constants.LANDING_THRUST)




