from datetime import datetime, timedelta

#initializes the truck object
class Truck:
    def __init__(self, truck_id, capacity, speed, start_time):
        self.id = truck_id
        self.capacity = capacity
        self.speed = speed
        self.packages = []
        self.current_location = "HUB"
        self.mileage = 0.0
        self.current_time = start_time
        self.available_time = start_time

#implements removal of packages. Will be manually loading trucks
        def remove_package(self, package):
            if package in self.packages:
                self.packages.remove(package)
                return True
            return False

#implements delivery of packages
        def deliver_package(self, package, distance):
            travel_time = timedelta(hours = distance/self.speed)
            self.current_time += travel_time
            self.milage += distance
            self.current_location = package.destination
            package.deliver(self.current_time)
            self.packages.remove(package)

#implements returning to the hub
        def return_to_hub(self, distance_to_hub):
            travel_time = timedelta(hours = distance_to_hub / self.speed)
            self.current_time += travel_time
            self.mileage += distance_to_hub
            self.current_location = "HUB"
            self.available_time = self.current_time

#returns truck id, how many packages it has, how full it is, and how far it has driven
        def __str__(self):
            return f"Truck {self.id}: {len(self.packages)}/{self.capacity} packages, {self.mileage:.1f} miles"