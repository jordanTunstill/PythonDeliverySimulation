from datetime import datetime, timedelta


def calculate_distance(address1, address2, distances):
    # Normalize addresses by removing new lines, extra spaces, and converting to lowercase
    def normalize_address(address):
        return ' '.join(address.split()).strip().lower()

    address1_normalized = normalize_address(address1)
    address2_normalized = normalize_address(address2)

    # Find the closest matching address in the distances dictionary
    def find_closest_address(normalized_address, address_dict):
        for key in address_dict.keys():
            if normalized_address in normalize_address(key.lower()):
                return key
        raise KeyError(f"Address '{normalized_address}' not found in provided distances.")

    address1_key = find_closest_address(address1_normalized, distances)
    address2_key = find_closest_address(address2_normalized, distances[address1_key])

    return distances[address1_key][address2_key]


def find_nearest_package(current_location, undelivered_packages, package_table, distances):
    return min(undelivered_packages,
               key=lambda pid: calculate_distance(current_location, package_table.lookup(pid)['address'], distances))


def deliver_packages(trucks, package_table, distances, locations):
    hub_address = "western governors university 4001 south 700 east, salt lake city, ut 84107"

    for truck in trucks:
        truck.current_location = hub_address
        # Find all undelivered packages on the truck
        while truck.packages:
            nearest_package_id = find_nearest_package(truck.current_location, truck.packages, package_table, distances)
            package = package_table.lookup(nearest_package_id)

            # Calculate the nearest delivery address for an undelivered package on the truck
            distance = calculate_distance(truck.current_location, package['address'], distances)
            travel_time = timedelta(hours=distance / truck.speed)

            # Update the truck's mileage, time, and location to be at the nearest location
            truck.mileage += distance
            truck.current_time += travel_time
            truck.current_location = package['address']

            # Mark packages as delivered
            package['status'] = 'Delivered'
            package['delivery_time'] = truck.current_time

            # Remove the package from the truck
            truck.packages.remove(nearest_package_id)
            print(f"Truck {truck.id} delivered package {nearest_package_id} at {truck.current_time}")

        # Return the truck to the hub when it is empty
        distance_to_hub = calculate_distance(truck.current_location, hub_address, distances)
        truck.mileage += distance_to_hub
        truck.current_time += timedelta(hours=distance_to_hub / truck.speed)
        truck.current_location = hub_address
        print(f"Truck {truck.id} completed deliveries and returned to hub at {truck.current_time}. Total mileage: {truck.mileage:.1f}")
