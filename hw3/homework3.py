import sys
import string


def extract_words(text):
    return None # should return a list of words in the data sample.


class NbClassifier(object):

    def __init__(self, training_filename, stopword_file = None):
        self.attribute_types = set()
        self.label_prior = {}
        self.word_given_label = {}


        self.collect_attribute_types(training_filename, 1)
        self.train(training_filename)

    def collect_attribute_types(self, training_filename, k):
        self.attribute_types = set() # replace this

    def train(self, training_filename):
        self.label_prior = {} # replace this
        self.word_given_label = {} #replace this

    def predict(self, text):
        return {} #replace this


    def evaluate(self, test_filename):
        precision = 0.0
        recall = 0.0
        fscore = 0.0
        accuracy = 0.0
        return precision, recall, fscore, accuracy


def print_result(result):
    print("Precision:{} Recall:{} F-Score:{} Accuracy:{}".format(*result))


if __name__ == "__main__":

    classifier = NbClassifier(sys.argv[1])
    result = classifier.evaluate(sys.argv[2])
    print_result(result)
