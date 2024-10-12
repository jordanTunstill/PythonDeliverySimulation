class HashTable:
#initializes the hash table object
    def __init__(self, initial_size=40):
        self.size = initial_size
        self.count = 0
        self.table = [[] for _ in range(self.size)]
        self.load_factor_threshold = 0.7

#generates the hash index for the given key
    def _hash(self, key):
        return hash(key) % self.size

#resizes the hash index as needed
    def _resize(self, new_size):
        old_table = self.table
        self.size = new_size
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

#inserts the key pair into the hash table
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

#retrieves the value associated with the given key
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
#inserts the packages from the csv into the hash table
    def insert_package(self, id, address, deadline, city,
                       zipcode, weight, status):
        package_data = {
            'id' : id,
            'address': address,
            'deadline': deadline,
            'city': city,
            'zipcode': zipcode,
            'weight': weight,
            'status': status
        }

#returns the hash table
    def __str__(self):
        return str(self.table)