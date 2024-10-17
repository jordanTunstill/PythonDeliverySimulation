import codecs

def load_distance_data(distance_file, address_file):
    distances = {}
    addresses = {}

    # Load the address data
    with codecs.open(address_file, mode='r', encoding='utf-8-sig') as infile:
        for line in infile:
            parts = line.strip().split(',')
            if len(parts) == 3:
                index, name, address = parts
                addresses[int(index)] = f"{name}, {address}"

    # Load the distance data
    with codecs.open(distance_file, mode='r', encoding='utf-8-sig') as infile:
        for i, line in enumerate(infile):
            # Split by comma and convert to float
            distances[i] = [float(value) for value in line.strip().split(',') if value.strip()]

    print('Successfully loaded addresses and distances')
    return distances, addresses, {v: k for k, v in addresses.items()}