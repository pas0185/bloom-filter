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
        f = open(file_name, 'r')
        training_words = [line.replace('\n', '') for line in f]
        for word in training_words:
            self.add(word)

        return training_words

    def string_from_n_gram(self, n_gram):
        string = " "
        for n in n_gram:
            string += n + " "

        return string

    def filter_input_file(self, input_file):

        with open(input_file) as f:

            # Break apart file into list of single words, bigrams, and trigrams
            full_text = f.read()
            words = nltk.word_tokenize(full_text)

            filtered_words = [word for word in words if self.query(word)]
            filtered_bigrams = [bgram for bgram in nltk.bigrams(words) if self.query(' '.join(bgram))]
            filtered_trigrams = [tgram for tgram in nltk.trigrams(words) if self.query(' '.join(tgram))]


            # for line in textwrap.wrap(full_text, 140):
            #     print line

            return filtered_words

        pass

    def calculate_error_rate(self, removed_words, training_words):

        successes = 0
        failures = 0

        for removed in removed_words:
            if removed.lower() in training_words:
                # Successful filter!
                successes = successes + 1
            else:
                # False positive...
                failures = failures + 1


        error_rate = float(failures) / (successes + failures)

        return error_rate


if __name__ == '__main__':

    NUM_BITS        = 1000
    NUM_HASHES      = 5
    TRAINING_FILE   = "auto-words.txt"
    TEST_FILE       = "test-paragraph.txt"

    # Initialize the Bloom Filter
    bf = BloomFilter(NUM_BITS, NUM_HASHES)

    # Read the training file, return all of the training words
    training_words = bf.read_training_file(TRAINING_FILE)

    # Filter out a test paragraph, return words that were removed
    removed_words = bf.filter_input_file(TEST_FILE)

    error_rate = bf.calculate_error_rate(removed_words, training_words)
    print 'Error rate = %s' % error_rate

    pass
