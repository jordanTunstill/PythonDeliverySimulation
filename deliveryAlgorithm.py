from datetime import datetime, timedelta


def calculate_distance(address1, address2, distances):
    def normalize_address(address):
        return ' '.join(address.split()).strip().lower()

    def find_closest_address(normalized_address, address_dict):
        for key in address_dict.keys():
            if normalized_address in normalize_address(key) or normalize_address(key) in normalized_address:
                return key

        # If no exact match, try partial matching
        for key in address_dict.keys():
            if any(word in normalize_address(key) for word in normalized_address.split()):
                return key

        raise KeyError(f"Address '{normalized_address}' not found in provided distances.")

    address1_normalized = normalize_address(address1)
    address2_normalized = normalize_address(address2)

    address1_key = find_closest_address(address1_normalized, distances)
    address2_key = find_closest_address(address2_normalized, distances[address1_key])

    return distances[address1_key][address2_key]



def find_nearest_package(current_location, undelivered_packages, package_table, distances):
    return min(undelivered_packages,
               key=lambda pid: calculate_distance(current_location, package_table.lookup(pid)['address'], distances))


def deliver_packages(trucks, package_table, distances, locations):
    hub_address = "Western Governors University\n4001 South 700 East, \nSalt Lake City, UT 84107"  # Assuming the hub is the first location

    for truck in trucks:
        truck.current_location = hub_address
        truck.leave_hub()
        while truck.packages:
            nearest_package_id = find_nearest_package(truck.current_location, truck.packages, package_table, distances)
            package = package_table.lookup(nearest_package_id)

            distance = calculate_distance(truck.current_location, package['address'], distances)
            travel_time = timedelta(hours=distance / truck.speed)

            truck.mileage += distance
            truck.current_time += travel_time
            truck.current_location = package['address']

            package['status'] = 'Delivered'
            package['delivery_time'] = truck.current_time

            truck.packages.remove(nearest_package_id)
            print(f"Truck {truck.id} delivered package {nearest_package_id} at {truck.current_time}")

#special rule for package 9, to account for the right address being found after 10:20
            if nearest_package_id == 9 and truck.current_time >= datetime.strptime("10:20 AM", "%I:%M %p"):
                package['address'] = "410 S State St., Salt Lake City, UT 84111"

        distance_to_hub = calculate_distance(truck.current_location, hub_address, distances)
        truck.mileage += distance_to_hub
        truck.current_time += timedelta(hours=distance_to_hub / truck.speed)
        truck.current_location = hub_address
        print(f"Truck {truck.id} completed deliveries and returned to hub at {truck.current_time}. Total mileage: {truck.mileage:.1f}")