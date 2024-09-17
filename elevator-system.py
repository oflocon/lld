"""
The Direction enum represents the possible directions of elevator movement (UP or DOWN).
The Request class represents a user request for an elevator, containing the source floor and destination floor.
The Elevator class represents an individual elevator in the system. It has a capacity limit and maintains a list of 4. requests. The elevator processes requests concurrently and moves between floors based on the requests.
The ElevatorController class manages multiple elevators and handles user requests. It finds the optimal elevator to serve a request based on the proximity of the elevators to the requested floor.
The ElevatorSystem class is the entry point of the application and demonstrates the usage of the elevator system.

"""
from enum import Enum
from math import inf
from threading import Condition, Lock, Thread
import time

class Request():
    def __init__(self, source: int, destination: int) -> None:
        self.source = source 
        self.destination = destination
        

class Elevator():
    def __init__(self, id: int, capacity: int)-> None:
        self.id = id
        self.capacity = capacity
        self.current_floor = 0
        self.current_direction : Direction = None
        self.requests = []
        self._lock = Lock()
        self.condition = Condition(self._lock)

    def add_request(self, req : Request):
        with self._lock:
            if self.capacity > len(self.requests):
                print(f"req : {req.source} - {req.destination} added to elevator : {self.id}")
                self.requests.append(req)
                self.condition.notify_all()

    def serve_requests(self):
        print(f"elevator {self.id} starts working")
        while True:
            with self._lock:
                while self.requests:
                    current_req = self.requests[0]
                    self.requests.pop(0)
                    self.process_request(current_req)
                self.condition.wait()

        
    def process_request(self, req: Request):
        print(f"started processing request for source {req.source} destination {req.destination}")
        # first go from current_floor to source_floor
        if self.current_floor < req.source:
            self.current_direction = Direction.UP
            for floor in range(self.current_floor, req.source+1):
                print(f"currently reached floor : {floor} for elevator {self.id}")
                self.current_floor = floor
                time.sleep(1)
        else:
            self.current_direction = Direction.DOWN
            for floor in range(self.current_floor, req.source-1,-1):
                print(f"currently reached floor : {floor} for elevator {self.id}")
                self.current_floor = floor
                time.sleep(1)

        counter = 0
        if req.source > req.destination:
            self.current_direction = Direction.DOWN
            end_floor = req.destination-1
            counter = -1
        else:
            self.current_direction = Direction.UP
            end_floor = req.destination+1
            counter = 1

        for floor in range(req.source, end_floor, counter):
            print(f"currently reached floor : {floor} for elevator {self.id}")
            self.current_floor = floor
            time.sleep(1)
    
    def run(self):
        self.serve_requests()

class Floor():
    def __init__(self, level: int):
        self.level = level

    def add_request(self, destination_floor: int):
        pass
         
class Direction(Enum):
	UP = "UP"
	DOWN = "DOWN"


class ElevatorController():
    def __init__(self, number_of_elevators):
        self.elevators: Elevator = []
        self.number_of_elevators = number_of_elevators
        self.requests : Request = [] 
        for i in range (1,number_of_elevators+1):
            elevator = Elevator(i,5)
            self.elevators.append(elevator)
            Thread(target=elevator.run).start()

    def request_elevator(self, source: int, destination: int):
        assert source>=0 and source <= 10
        assert destination>=0 and destination <=10
        optimal_elevator = self.get_optimal_elevator(source, destination)
        print(f"optimal : {optimal_elevator.id}")
        if optimal_elevator:
            optimal_elevator.add_request(Request(source, destination))
        else:
            print("No elevator found")

    def get_optimal_elevator(self, source: int, destination: int) -> Elevator:
        min_dist = 100000
        # randomize better when all dist are same
        optimal_elevator = None
        for elevator in self.elevators:
            if min_dist > abs(elevator.current_floor - source):
                min_dist = abs(elevator.current_floor - source)
                optimal_elevator = elevator
        return optimal_elevator
    

class ElevatorDemo():
    def __init__(self) -> None:
        controller = ElevatorController(5)
        controller.request_elevator(5, 10)
        controller.request_elevator(2,8)
        controller.request_elevator(4,2)

if __name__ == "__main__":
    ElevatorDemo()

