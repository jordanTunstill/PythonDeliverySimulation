from datetime import datetime, timedelta
from hashTable import HashTable
from package import Package
from truck import Truck
from loader import load_distance_data
from deliveryAlgorithm import deliver_packages


def initialize_trucks(start_time):
    start_time1 = datetime(2024, 10, 11, 8, 0)   # 8:00 AM
    start_time2 = datetime(2024, 10, 11, 9, 5)   # 9:05 AM
    start_time3 = datetime(2024, 10, 11, 10, 20) # 10:20 AM

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
    trucks[0].packages = [1, 13, 14, 15, 16, 19, 20, 21, 31, 4, 40, ]
    trucks[1].packages = [3, 18, 36, 38, 29, 30, 34, 8, 37, 5, 7, 39, 33, 25, 28]
    trucks[2].packages = [9, 2, 10, 11, 12, 17, 22, 32, 6, 23, 24, 26, 27, 35]


# this checks the status of the packages, using the previous lookup package
def check_package_status(package_table, package_id, time):
    package_information = package_lookup(package_table, package_id)
    if package_information:
        # status = package_information(package_delivery_status) #i still need to implement the actual checker.
        # print(f"Package {package_id} status at {time}: {status}")
        print(f"Delivery Address: {package_information['package_address']}")
        print(f"Delivery Deadline: {package_information['deadline']}")
        print(f"Delivery City: {package_information['city']}")
        print(f"Delivery Zipcode: {package_information['zipcode']}")
        print(f"Delivery Weight: {package_information['weight']}")
        print(f"Delivery Status: {package_information['status']}")
        print(f"Delivery Special Notes: {package_information['special_notes']}")
    else:
        print(f"Package {package_id} not found")


# implements a viewer for total mileage of the trucks
def view_total_mileage(trucks):
    total_mileage = sum(truck.mileage for truck in trucks)
    print(f"Total Mileage for all trucks: {total_mileage:.1f} miles")


def main():
    # initialization of hash table
    package_table = HashTable(csv_filename="WGUPS Package File.csv")

    # loads distance data from file
    distances, locations, location_to_index = load_distance_data("WGUPS-Distance-Table-Filled.csv",
                                                                 "WGUPS-Addresses.csv")
    #loads address data from file

    # daily start time for the trucks
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
        print("2. Check package status")
        print("3. View total mileage")
        print("4. Exit")
        choice = input("Enter your choice: ")

        # this tells users if the simulation has been run, and is not visible once it has been run, as it can only be run once
        if choice == '1' and not simulation_run:
            deliver_packages(trucks, package_table, distances, locations)
            print("Delivery simulation completed.")
            simulation_run = True

        # this allows users to check the delivery info for a package at a given time, if the simulation has been run
        elif choice == '2':
            if simulation_run:
                package_id = input("Enter package ID: ")
                time = input("Enter time (HH:MM): ")
                check_package_status(package_table, package_id, time)
            else:
                print("Please run the simulation first.")

        # this allows users to check the mileage of the trucks at a given time, if the simulation has been run
        elif choice == '3':
            if simulation_run:
                view_total_mileage(trucks)
            else:
                print("Please run the simulation first.")

        # this ends the program, and includes a break statement for the overall loop for error handling
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
