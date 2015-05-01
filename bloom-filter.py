__author__ = 'Patrick Sheehan'

# Patrick Sheehan
# May 1, 2015
# CSCE 438 HW #4
#
# Sources:
#
# Wikipedia - http://en.wikipedia.org/wiki/Bloom_filter
# Bitarray - https://pypi.python.org/pypi/bitarray/
# MurmurHash3 - https://pypi.python.org/pypi/mmh3/2.0
# Natural Language Toolkit - http://www.nltk.org/
# Piazza - TAMU CSCE 438
#

from bitarray import bitarray
import mmh3
import nltk
import textwrap

class BloomFilter:

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

        # "To add an element, feed it to each of the k hash functions to get k array positions.
        # Set the bits at all these positions to 1"
        for seed in range(self.num_hashes):
            # Modulus for remainder if hash is larger than bit array
            hash = mmh3.hash(element.lower(), seed) % self.num_bits
            self.bit_array[hash] = 1

        pass

    def query(self, element):
        # Test whether an element is in the set

        # "Feed [the element] to each of the k hash functions to get k array positions.
        for seed in range(self.num_hashes):
            hash = mmh3.hash(element.lower(), seed) % self.num_bits

            # If any of the bits at these positions is 0, the element is definitely not in the set.
            # If it were, then all the bits would have been set to 1 when it was inserted.
            if self.bit_array[hash] == 0:
                # print 'The element %s is definitely not in the set' % element
                return False

        # If all are 1, then either the element is in the set, or the bits have by chance been set to 1
        # during the insertion of other elements resulting in a false positive."
        # print 'The element %s is probably in the set' % element
        return True

    def read_training_file(self, file_name):
        # Input a training file with n-grams newline-delimited

        with open(file_name) as f:
            for word in nltk.word_tokenize(f.read().strip('\n')):
                # Add each to the bit_array
                
                self.add(word)
        pass

    def filter_input_file(self, input_file):

        with open(input_file) as f:

            # Break apart file into list of single words, bigrams, and trigrams
            full_text = f.read().strip('\n')
            words = nltk.word_tokenize(full_text)

            filtered_text = ""

            for word in words:
                filtered_text += "****" if self.query(word) else word
                filtered_text += " "

            # bigrams = nltk.bigrams(words)
            # trigrams = nltk.trigrams(words)

            for line in textwrap.wrap(filtered_text, 140):
                print line

        pass


if __name__ == '__main__':

    NUM_BITS        = 1000
    NUM_HASHES      = 5
    TRAINING_FILE   = "auto-words.txt"
    TEST_FILE       = "test-paragraph.txt"

    bf = BloomFilter(NUM_BITS, NUM_HASHES)
    bf.read_training_file(TRAINING_FILE)

    bf.filter_input_file(TEST_FILE)

    pass
