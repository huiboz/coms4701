import sys
import string
import math


def extract_words(text):
    text = text.lower() # convert to lower case


    for p in string.punctuation: # strip the punctuation
        text = text.replace(p,"")

    return text.split() # return a list splitting on white spaces


class NbClassifier(object):

    def __init__(self, training_filename, stopword_file = None):
        self.attribute_types = set()
        self.label_prior = {}
        self.word_given_label = {}

        self.collect_attribute_types(training_filename, 1)
        self.train(training_filename)

    def collect_attribute_types(self, training_filename, k):
        count_dic = {}
        vocabulary = set()
        with open(training_filename,'r') as f:
            for line in f:
                line = line.strip()
                list_line = extract_words(line)
                list_line.pop(0) # remove the first word 'ham' or 'spam'
                for word in list_line:
                    if (word in count_dic):
                        count_dic[word] = count_dic[word] + 1
                    else:
                        count_dic[word] = 1

        for key in count_dic:
            if (count_dic[key] >= k):
                vocabulary.add(key)

        self.attribute_types = vocabulary

    def train(self, training_filename):
        c = 1
        vocabulary_size = len(self.attribute_types)

        ham_dic = {}
        spam_dic = {}
        ham_count = 0
        spam_count = 0
        ham_word_count = 0
        spam_word_count = 0
        with open(training_filename,'r') as f:
            for line in f:
                line = line.strip()
                list_line = extract_words(line)
                first_word = list_line.pop(0)

                if first_word == 'ham':
                    ham_count = ham_count + 1
                    for word in list_line:
                        if (word in self.attribute_types):
                            if (word in ham_dic):
                                ham_dic[word] = ham_dic[word] + 1
                            else:
                                ham_dic[word] = 1
                            ham_word_count = ham_word_count + 1

                if first_word == 'spam':
                    spam_count = spam_count + 1
                    for word in list_line:
                        if (word in self.attribute_types):
                            if (word in spam_dic):
                                spam_dic[word] = spam_dic[word] + 1
                            else:
                                spam_dic[word] = 1
                            spam_word_count = spam_word_count + 1

        total_count = ham_count + spam_count
        self.label_prior['spam'] = spam_count / total_count
        self.label_prior['ham'] = ham_count / total_count

        for word in self.attribute_types:
            ham_count = c
            spam_count = c
            if (word in ham_dic):
                ham_count = ham_dic[word] + c
            if (word in spam_dic):
                spam_count = spam_dic[word] + c
            self.word_given_label[(word,'ham')] = ham_count /     \
                                    (ham_word_count + c * vocabulary_size)
            self.word_given_label[(word,'spam')] = spam_count /     \
                                    (spam_word_count + c * vocabulary_size)


    def predict(self, text):
        list_line = extract_words(text)
        label = list_line.pop(0)

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
