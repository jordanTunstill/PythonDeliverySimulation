#Jordan Tunstill 012227272
from datetime import datetime, timedelta
from hashTable import HashTable
from package import Package
from truck import Truck
from loader import load_distance_data
from deliveryAlgorithm import deliver_packages, get_current_address


def initialize_trucks(start_time):
    start_time1 = datetime(2024, 10, 11, 8, 0)   # 8:00 AM
    start_time2 = datetime(2024, 10, 11, 9, 1)   # 9:05 AM
    start_time3 = datetime(2024, 10, 11, 10, 21) # 10:20 AM

    return [
        Truck(1, 16, 18, start_time1),
        Truck(2, 16, 18, start_time2),
        Truck(3, 16, 18, start_time3)
    ]


# this is the lookup package to ensure that package are being loaded
def package_lookup(package_table, package_id):
    package = package_table.lookup(package_id)
    if package:
        return {
            'package_address': package['address'],
            'deadline': package['deadline'],
            'city': package['city'],
            'zipcode': package['zipcode'],
            'weight': package['weight'],
            'status': package['status'],
            'special_notes': package['special_notes']
        }
    else:
        return None


def load_trucks(trucks, package_table):
    trucks[0].packages = [1, 13, 14, 15, 16, 19, 20, 21, 31, 4, 40, 39, 8, 30, 37]
    trucks[1].packages = [3, 6, 18, 36, 38, 29, 34, 5, 7, 33, 25, 28]
    trucks[2].packages = [9, 2, 10, 11, 12, 17, 22, 32, 23, 24, 26, 27, 35]


# this checks the status of the packages, using the previous lookup package
def check_package_status(package_table, check_time):
    while True:
        try:
            package_id = int(input("Enter package ID (or 0 to return to main menu): "))
            if package_id == 0:
                return  # This will exit the function and return to the main menu

            package = package_table.lookup(package_id)
            if package is None:
                print(f"Package with ID {package_id} not found.")
                continue

            # Determine status based on times and stored status
            current_address = get_current_address(package, check_time)
            status = package['status']
            if status == 'Delivered' and check_time < package['delivery_time']:
                status = 'En Route' if check_time >= package.get('departure_time', check_time) else 'At Hub'

            print(f"\nPackage {package_id} status at {check_time.strftime('%Y-%m-%d %I:%M:%S %p')}:")
            print(f"Address: {current_address}")
            print(f"Deadline: {package['deadline']}")
            print(f"City: {package['city']}")
            print(f"Zip Code: {package['zipcode']}")
            print(f"Weight: {package['weight']}")
            print(f"Status: {status}")

            if package['special_note']:
                print(f"Special Notes: {package['special_note']}")

            if status == "Delivered":
                print(f"Delivered at: {package['delivery_time'].strftime('%Y-%m-%d %I:%M:%S %p')}")
            elif status == "En Route" and 'departure_time' in package:
                print(f"Departed at: {package['departure_time'].strftime('%Y-%m-%d %I:%M:%S %p')}")

            # Ask if the user wants to check another package
            another = input("\nDo you want to check another package? (y/n): ").lower()
            if another != 'y':
                return  # This will exit the function and return to the main menu

        except ValueError:
            print("Invalid input. Please enter a valid package ID.")


def show_packages_status_on_trucks(trucks, package_table, check_time):
    print(f"\nPackage Status at {check_time.strftime('%Y-%m-%d %I:%M:%S %p')}:\n")

    # Create a dictionary to group packages by truck
    packages_by_truck = {truck.id: [] for truck in trucks}

    # Iterate through all packages and assign them to trucks
    for package_id in range(1, 41):
        package = package_table.lookup(package_id)
        if package is None:
            continue

        # Determine current status
        if package.get('delivery_time') and check_time >= package['delivery_time']:
            status = "DELIVERED"
            extra_info = f", Delivered at: {package['delivery_time'].strftime('%Y-%m-%d %I:%M:%S %p')}"
        elif package.get('departure_time') and check_time >= package['departure_time']:
            status = "EN ROUTE"
            extra_info = f", Departed at: {package['departure_time'].strftime('%Y-%m-%d %I:%M:%S %p')}"
        else:
            status = "AT HUB"
            extra_info = ""

        truck_id = package.get('assigned_truck')
        packages_by_truck[truck_id].append((package_id, status, extra_info))

    # Display packages for each truck
    for truck_id, packages in packages_by_truck.items():
        print(f"Truck {truck_id}:")

        if not packages:
            print("  No packages")
        else:
            for package_id, status, extra_info in packages:
                print(f"  Package {package_id}: {status}{extra_info}")
        print()

# implements a viewer for total mileage of the trucks
def view_total_mileage(trucks):
    total_mileage = sum(truck.mileage for truck in trucks)
    print(f"Total Mileage for all trucks: {total_mileage:.1f} miles")


def main():
    # initialization of hash table
    package_table = HashTable(csv_filename="WGUPS Package File.csv")

    # loads distance data from file
    distances, addresses, location_to_index = load_distance_data("WGUPS-Distance-Table-Filled.csv",
                                                                 "WGUPS-Addresses.csv")
    #loads address data from file

    # daily start time for the trucks, though i have overwritten this with unique start times
    start_time = datetime(2024, 10, 11, 8, 0)

    # initialize the trucks
    trucks = initialize_trucks(start_time)

    #loads the trucks
    load_trucks(trucks, package_table)

    # returns truck information
    for truck in trucks:
        print(f"Truck {truck.id}: {len(truck.packages)}/{truck.capacity} packages, {truck.mileage:.1f} miles")

    # begin the program
    simulation_run = False

    # this is the CLI
    while True:
        print("\nWGUPS Package Delivery System")
        if not simulation_run:
            print("1. Start delivery simulation")
        print("2. Check individual package information")
        print("3. Check packages on each truck")
        print("4. View total mileage")
        print("5. Exit")
        choice = input("Enter your choice: ")

        # this tells users if the simulation has been run, and is not visible once it has been run, as it can only be run once
        if choice == '1' and not simulation_run:
            deliver_packages(trucks, package_table, distances, addresses)
            print("Delivery simulation completed.")
            simulation_run = True

        # this allows users to check the delivery info for a package at a given time, if the simulation has been run
        elif choice == '2':
            check_time_str = input("Enter time to check status (HH:MM): ")
            if not check_time_str:
                print("No time entered. Returning to main menu.")
                continue

            try:
                check_time = datetime.strptime(check_time_str, '%H:%M')
                check_time = check_time.replace(year=2024, month=10, day=11)
            except ValueError:
                print("Invalid time format. Please use HH:MM.")
                continue

            if simulation_run:
                check_package_status(package_table, check_time)
            else:
                print("Please run the simulation first.")

        elif choice == '3':
            if simulation_run:
                check_time_str = input("Enter time to check status (HH:MM): ")
                try:
                    check_time = datetime.strptime(check_time_str, '%H:%M')
                    check_time = check_time.replace(year=2024, month=10,
                                                    day=11)  # Use the same date as in your simulation
                    show_packages_status_on_trucks(trucks, package_table, check_time)
                except ValueError:
                    print("Invalid time format. Please use HH:MM.")
            else:
                print("Please run the simulation first.")

        # this allows users to check the mileage of the trucks at a given time, if the simulation has been run
        elif choice == '4':
            if simulation_run:
                view_total_mileage(trucks)
            else:
                print("Please run the simulation first.")

        # this ends the program, and includes a break statement for the overall loop for error handling
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
