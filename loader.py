import csv

def clean_address(address):
    # This cleans address by removing unnecessary newlines and spaces.
    return address.replace('\n', ' ').strip()

# This loads the distance table, which has been cleaned to read properly.
def load_distance_data(filename):
    distances = {}
    locations = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        locations = [' '.join(loc.split('\n')).strip() for loc in next(reader)[1:]]

        for row in reader:
            from_location = ' '.join(row[0].split('\n')).strip()
            distances[from_location] = {' '.join(locations[i].split('\n')).strip(): float(dist) if dist else 0
                                        for i, dist in enumerate(row[1:]) if dist}

    return distances, locations

def load_address_data():
    addresses = [
        "Western Governors University\n4001 South 700 East,\nSalt Lake City, UT 84107",
        "International Peace Gardens\n1060 Dalton Ave S",
        "Sugar House Park\n1330 2100 S",
        "Taylorsville-Bennion Heritage City Gov Off\n1488 4800 S",
        "Salt Lake City Division of Health Services\n177 W Price Ave",
        "South Salt Lake Public Works\n195 W Oakland Ave",
        "Salt Lake City Streets and Sanitation\n2010 W 500 S",
        "Deker Lake\n2300 Parkway Blvd",
        "Salt Lake City Ottinger Hall\n233 Canyon Rd",
        "Columbus Library\n2530 S 500 E",
        "Taylorsville City Hall\n2600 Taylorsville Blvd",
        "South Salt Lake Police\n2835 Main St",
        "Council Hall\n300 State St",
        "Redwood Park\n3060 Lester St",
        "Salt Lake County Mental Health\n3148 S 1100 W",
        "Salt Lake County/United Police Dept\n3365 S 900 W",
        "West Valley Prosecutor\n3575 W Valley Central Sta bus Loop",
        "Housing Auth. of Salt Lake County\n3595 Main St",
        "Utah DMV Administrative Office\n380 W 2880 S",
        "Third District Juvenile Court\n410 S State St",
        "Cottonwood Regional Softball Complex\n4300 S 1300 E",
        "Holiday City Office\n4580 S 2300 E",
        "Murray City Museum\n5025 State St",
        "Valley Regional Softball Complex\n5100 South 2700 West",
        "City Center of Rock Springs\n5383 South 900 East #104",
        "Rice Terrace Pavilion Park\n600 E 900 South",
        "Wheeler Historic Farm\n6351 South 900 East"
    ]
    return [clean_address(address) for address in addresses]