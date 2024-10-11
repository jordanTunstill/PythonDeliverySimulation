class HashTable:
#initializes the hash table object
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

#generates the hash index for the given key
    def _hash(self, key):
        return hash(key) % self.size

#inserts the key pair into the hash table
    def insert(self, key, value):
        hash_index = self._hash(key)
        for item in self.table[hash_index]:
            if item[0] == key:
                item[1] = value
                return
        self.table[hash_index].append([key, value])

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
                return True
        return False

 # checks if the hash table contains a key
    def contains(self, key):
        hash_index = self._hash(key)
        for item in self.table[hash_index]:
            if item[0] == key:
                return True
        return False

#returns the hash table
    def __str__(self):
        return str(self.table)