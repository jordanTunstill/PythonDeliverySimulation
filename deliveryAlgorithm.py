from datetime import datetime, timedelta
import csv
import codecs

def calculate_distance(address1, address2, distances, addresses):
    def find_address_index(address):
        # Remove apartment numbers and zip codes for matching
        simplified_address = ' '.join(address.split(',')[0].split()[:-1]).lower()
        for index, full_address in addresses.items():
            if simplified_address in full_address.lower():
                return index
        return None

    index1 = find_address_index(address1)
    index2 = find_address_index(address2)

    if index1 is None:
        raise KeyError(f"Address not found: {address1}")
    if index2 is None:
        raise KeyError(f"Address not found: {address2}")

    return float(distances[index1][index2])

# Load addresses
def load_addresses(address_file):
    addresses = {}
    with codecs.open(address_file, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) == 3:
                index, name, address = row
                addresses[int(index)] = f"{name}, {address}"
    return addresses

# Load distances
def load_distances(distance_file):
    distances = {}
    with codecs.open(distance_file, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        for i, row in enumerate(csv_reader):
            distances[i] = {j: float(d) if d else 0 for j, d in enumerate(row)}
    return distances

# Usage
addresses = load_addresses("WGUPS-Addresses.csv")
distances = load_distances("WGUPS-Distance-Table-Filled.csv")

def get_current_address(package, current_time):
    if package['id'] == 9 and current_time.time() >= datetime.strptime("10:20", "%H:%M").time():
        return '410 S State St, Salt Lake City, UT 84111'
    return package['address']

def find_nearest_package(current_location, undelivered_packages, package_table, distances, addresses):
    return min(undelivered_packages,
               key=lambda pid: calculate_distance(current_location, package_table.lookup(pid)['address'], distances, addresses))

def deliver_packages(trucks, package_table, distances, addresses):
    hub_address = "4001 South 700 East"

    for truck in trucks:
        truck.current_location = hub_address
        print(f"Truck {truck.id} leaving the hub to start deliveries at {truck.current_time.strftime('%I:%M %p')}")

        # Set departure time and status for all packages on this truck
        for package_id in truck.packages:
            package = package_table.lookup(package_id)
            if package is not None:
                package['status'] = 'En Route'
                package['departure_time'] = truck.current_time
                package['assigned_truck'] = truck.id

        while truck.packages:
            nearest_package_id = find_nearest_package(truck.current_location, truck.packages, package_table, distances, addresses)
            package = package_table.lookup(nearest_package_id)
            current_address = get_current_address(package, truck.current_time)
            distance = calculate_distance(truck.current_location, current_address, distances, addresses)
            travel_time = timedelta(hours=distance / truck.speed)

            # Update current time before delivery
            truck.current_time += travel_time
            truck.mileage += distance
            truck.current_location = current_address

            package['status'] = 'Delivered'
            package['delivery_time'] = truck.current_time

            print(f"Truck {truck.id} delivered package {nearest_package_id} at {truck.current_time.strftime('%Y-%m-%d %I:%M:%S %p')}")
            truck.packages.remove(nearest_package_id)

        # Return to hub
        distance_to_hub = calculate_distance(truck.current_location, hub_address, distances, addresses)
        travel_time_to_hub = timedelta(hours=distance_to_hub / truck.speed)
        truck.mileage += distance_to_hub
        truck.current_time += travel_time_to_hub
        truck.current_location = hub_address
        print(f"Truck {truck.id} completed deliveries and returned to hub at {truck.current_time.strftime('%Y-%m-%d %I:%M:%S %p')}. Total mileage: {truck.mileage:.1f}")