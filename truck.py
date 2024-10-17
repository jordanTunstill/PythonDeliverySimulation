

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
        self.departure_time = None

    def leave_hub(self):
        self.departure_time = self.available_time
        print(f"Truck {self.id} leaving the hub to start deliveries at {self.departure_time.strftime('%I:%M %p')}")

#returns truck id, how many packages it has, how full it is, and how far it has driven
        def __str__(self):
            return f"Truck {self.id}: {len(self.packages)}/{self.capacity} packages, {self.mileage:.1f} miles"