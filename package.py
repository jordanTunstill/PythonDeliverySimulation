from datetime import datetime, timedelta

#most of this is outdated by changes made to the other files, but everything runs very well together.

class Package:
#this initializes the package object for use in the other files
    def __init__(self, package_id, address, deadline, city, zipcode, weight, special_notes):
        self.id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipcode = zipcode
        self.weight = weight
        self.status = "AT HUB"
        self.special_notes = special_notes
        self.delivery_time = None
        self.departure_time = None

#this indicates if package is delivered
    def deliver(self, time):
        self.status = "DELIVERED"
        self.delivery_time = time

#this indicates if package is en route
    def en_route(self, time):
        self.status = "EN ROUTE"
        self.departure_time = time

#this gets the status of a package
    def get_status(self, current_time):
        if self.delivery_time and current_time >= self.delivery_time:
            return "DELIVERED"
        elif self.departure_time and current_time >= self.departure_time:
            return "EN ROUTE"
        else:
            return "AT HUB"

#this is special handling for package 9
    def get_current_address(package, current_time):
        if package['id'] == 9 and current_time.time() >= datetime.strptime("10:20", "%H:%M").time():
            return '410 S State St, Salt Lake City, UT 84111'
        return package['address']

#this returns information about the given package
    def __str__(self):
        status_str = f"Status: {self.status}"
        if self.status == "DELIVERED" and self.delivery_time:
            status_str += f" at {self.delivery_time.strftime('%H:%M')}"
        return f"Package {self.id}: {self.address}, {self.city} {self.zipcode}, Due: {self.deadline}, Weight: {self.weight}, {status_str}"