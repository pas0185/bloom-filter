__author__ = 'Patrick Sheehan'

from bitarray import bitarray
import mmh3

class BloomFiler:


    def __init__(self, num_bits, num_hashes):
        # Initialize bitarray with the given size

        # Set how many hash functions should be used


        pass

    def add(self, element):
        # Add an n-gram from some training data

        # From Wikipedia:
        # "To add an element, feed it to each of the k hash functions to get k array positions.
        # Set the bits at all these positions to 1"

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

if __name__ == '__main__':

    pass
