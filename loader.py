import codecs

#this is used to load the distance and address data into the project, from the csv files
def load_distance_data(distance_file, address_file):
    distances = {}
    addresses = {}

#this loads the address data
    with codecs.open(address_file, mode='r', encoding='utf-8-sig') as infile:
        for line in infile:
            parts = line.strip().split(',')
            if len(parts) == 3:
                index, name, address = parts
                addresses[int(index)] = f"{name}, {address}"

#this loads the distance data
    with codecs.open(distance_file, mode='r', encoding='utf-8-sig') as infile:
        for i, line in enumerate(infile):
#this splits the data by comma and convert to float
            distances[i] = [float(value) for value in line.strip().split(',') if value.strip()]

    print('Successfully loaded addresses and distances')
    return distances, addresses, {v: k for k, v in addresses.items()}