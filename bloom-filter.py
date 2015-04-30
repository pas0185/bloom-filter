__author__ = 'Patrick Sheehan'

# Sources:
# Bitarray Documentation:
# https://pypi.python.org/pypi/bitarray/
#
# MurmurHash3 Documentation:
# https://pypi.python.org/pypi/mmh3/2.0
#

from bitarray import bitarray
import mmh3

class BloomFiler:


    def __init__(self, num_bits, num_hashes):
        # Initialize bitarray of num_bits size with all set to 0/False
        self.num_bits = num_bits
        self.bit_array = bitarray(num_bits)
        self.bit_array.setall(0)

        # Set how many hash functions should be used
        self.num_hashes = num_hashes

        pass

    def add(self, element):
        # Add an n-gram from some training data

        # From Wikipedia:
        # "To add an element, feed it to each of the k hash functions to get k array positions.
        # Set the bits at all these positions to 1"

        for seed in [i for i in range(self.num_hashes)]:
            # Modulus for remainder if hash is larger than bit array
            hash = mmh3.hash(element, seed) % self.num_bits
            self.bit_array[hash] = 1

        pass

    def query(self, element):
        # Test whether an element is in the set

        # From Wikipedia:
        # "Feed it [the element] to each of the k hash functions to get k array positions.


        # If any of the bits at these positions is 0, the element is definitely not in the set.
        # If it were, then all the bits would have been set to 1 when it was inserted.

        # If all are 1, then either the element is in the set, or the bits have by chance been set to 1
        # during the insertion of other elements resulting in a false positive."

        pass

    def read_training_file(self, file_name):
        # Input a training file with n-grams newline-delimited

        # Add each to the bit_array


        pass

if __name__ == '__main__':

    pass
