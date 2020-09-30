class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        self.capacity = MIN_CAPACITY
        self.hash_table = [None] * self.capacity
        self.size = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return len(self.hash_table)


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        return self.size / self.get_num_slots()


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """

        # The reason we use 5381 is because it happens to be a "magic constant" that results in few collisions :P
        hash = 5381

        for x in key:
            # Bitwise shift operator <<
            # Bits shifted to the left by 5 places
            hash = ((hash << 5) + ord(x))
        
        return hash


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        # Not using fnv1
        # return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        key_sum = self.hash_index(key)

        node = self.hash_table[key_sum]

        self.size += 1

        if node is None:
            self.hash_table[key_sum] = HashTableEntry(key, value)
            return None
        if node.key == key:
            self.hash_table[key_sum] = HashTableEntry(key, value)
            self.size -= 1

        prev = node

        while node is not None:
            prev = node
            node = node.next
        prev.next = HashTableEntry(key, value)


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        key_hashed = self.hash_index(key)

        deleted = self.hash_table[key_hashed]

        prev = None

        while deleted is not None and deleted.key != key:
            prev = deleted
            deleted = deleted.next
        if deleted is None:
            return None
        else:
            self.size -= 1
            res = deleted.value
            if prev is None:
                self.hash_table[key_hashed] = deleted.next
            else:
                prev.next = prev.next.next
            return res


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        key_hashed = self.hash_index(key)

        node = self.hash_table[key_hashed]

        while node is not None and node.key != key:
            node = node.next
        if node is None:
            return None
        else:
            return node.value


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        if self.get_load_factor() > 0.7:
            old_hash_table = self.hash_table
            self.hash_table = [None] * new_capacity
            for node in old_hash_table:
                while node.next:
                    self.put(node.key, node.value)
                    node = node.next
                self.put(node.key, node.value)



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
