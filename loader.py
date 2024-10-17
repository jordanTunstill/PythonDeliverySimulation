import csv

def load_distance_data(distance_file, address_file):
    distances = {}
    locations = []
    location_to_index = {}

    def normalize_address(address):
        return ' '.join(address.split()).strip().lower()

    # Load locations first
    with open(address_file, mode='r') as infile:
        content = infile.read()
        address_entries = content.split('"')[1::2]  # Split by quotes and take every other item

        for index, entry in enumerate(address_entries):
            lines = entry.strip().split('\n')
            if len(lines) >= 2:
                location = lines[0].strip()
                address = ' '.join(line.strip() for line in lines[1:])
                normalized_address = normalize_address(f"{location}, {address}")
                locations.append(normalized_address)
                location_to_index[normalized_address] = index
            else:
                print(f"Warning: Invalid address entry: {entry}")

    # Load distance data
    with open(distance_file, mode='r') as infile:
        reader = csv.reader(infile)
        headers = next(reader)

        for i, row in enumerate(reader):
            from_location = locations[i]
            distances[from_location] = {
                locations[j]: float(value) if value.strip() else 0.0
                for j, value in enumerate(row) if j != i
            }
    print(f"Successfully loaded addresses and distances")
    return distances, locations, location_to_index

