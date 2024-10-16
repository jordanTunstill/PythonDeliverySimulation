import csv

class HashTable:
# initializes the hash table object
    def __init__(self, initial_size=40, csv_filename=None):
        self.size = initial_size
        self.count = 0
        self.table = [[] for _ in range(self.size)]
        self.load_factor_threshold = 0.7
        if csv_filename:
            self.read_csv(csv_filename)

# generates the hash index for the given key
    def _hash(self, key):
        return hash(key) % self.size

# resizes the hash index as needed
    def _resize(self, new_size):
        old_table = self.table
        self.size = new_size
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

# inserts the key pair into the hash table
    def insert(self, key, value):
        if self.count / self.size >= self.load_factor_threshold:
            self._resize(self.size * 2)

        hash_index = self._hash(key)
        for item in self.table[hash_index]:
            if item[0] == key:
                item[1] = value
                return
        self.table[hash_index].append([key, value])
        self.count += 1

# retrieves the value associated with the given key
    def lookup(self, key):
        hash_index = self._hash(key)
        for item in self.table[hash_index]:
            if item[0] == key:
                return item[1]
        return None

# removes a key-value pair from the hash table
    def remove(self, key):
        hash_index = self._hash(key)
        for i, item in enumerate(self.table[hash_index]):
            if item[0] == key:
                del self.table[hash_index][i]
                self.count -= 1
                return True
        return False

# checks if the hash table contains a key
    def contains(self, key):
        hash_index = self._hash(key)
        for item in self.table[hash_index]:
            if item[0] == key:
                return True
        return False

# inserts the packages from the csv into the hash table
    def insert_package(self, id, address, deadline, city,
                       state, zipcode, weight, status, special_note=''):
        package_data = {
            'id': id,
            'address': address,
            'deadline': deadline,
            'city': city,
            'state': state,
            'zipcode': zipcode,
            'weight': weight,
            'status': status,
            'special_note': special_note
        }
        self.insert(id, package_data)

# reads the csv file and imports the data to the hash table
    def read_csv(self, filename):
        try:
            print(f"Attempting to read file: {filename}")
            with open(filename, 'r') as infile:
                print("File opened successfully. Starting to read rows.")
                reader = csv.reader(infile)
                for row in reader:
                    if len(row) < 7:
                        print(f"Row invalid. Skipping row: {row}")
                        continue

                    package_id = int(row[0])
                    address = row[1]
                    city = row[2]
                    state = row[3]
                    zipcode = row[4]
                    deadline = row[5]
                    weight = row[6]
                    status = 'At hub'
                    special_note = row[7] if len(row) > 7 else ''

# This shows that the table worked
                    self.insert_package(package_id, address, deadline, city, state,
                                        zipcode, weight, status, special_note)
                    print(f"Inserted package {package_id}")

            print(f"Successfully loaded {self.count} packages from {filename}")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")
        except ValueError as e:
            print(f"Error parsing data: {e}")
            print(f"Problem in row: {row}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            print(f"Problem in row: {row}")


    def __str__(self):
         return str(self.table)