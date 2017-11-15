'''
original test with c = 1 k = 1
on dev.txt: Precision:0.9508196721311475
Recall:0.8656716417910447 F-Score:0.9062499999999999 Accuracy:0.9784560143626571
on test.txt: Precision:0.9491525423728814
Recall:0.8888888888888888 F-Score:0.9180327868852458 Accuracy:0.9820466786355476
'''

'''
after tuning test with c = 0.08 k = 1
on dev.txt: Precision:0.9672131147540983
Recall:0.8805970149253731 F-Score:0.9218749999999999 Accuracy:0.9820466786355476
on test.txt: Precision:0.9655172413793104
Recall:0.8888888888888888 F-Score:0.9256198347107438 Accuracy:0.9838420107719928
'''




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
        self.stopword_file = stopword_file

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

        stop = set()
        with open(self.stopword_file,'r') as f:
            for line in f:
                line = line.strip()
                list_line = extract_words(line)
                stop.add(list_line.pop(0))

        for stop_word in stop:
            if stop_word in vocabulary:
                vocabulary.remove(stop_word)

        self.attribute_types = vocabulary

    def train(self, training_filename):
        c = 0.08
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
            ham_word = c
            spam_word = c
            if (word in ham_dic):
                ham_word = ham_dic[word] + c
            if (word in spam_dic):
                spam_word = spam_dic[word] + c
            self.word_given_label[(word,'ham')] = ham_word /     \
                                    (ham_word_count + c * vocabulary_size)
            self.word_given_label[(word,'spam')] = spam_word /     \
                                    (spam_word_count + c * vocabulary_size)


    def predict(self, text):
        list_line = extract_words(text)
        p_ham = math.log(self.label_prior['ham'])
        p_spam = math.log(self.label_prior['spam'])

        for word in list_line:
            if (word in self.attribute_types):
                p_ham = p_ham + math.log(self.word_given_label[(word,'ham')])
                p_spam = p_spam + math.log(self.word_given_label[(word,'spam')])


        if p_spam > p_ham:
            return 'spam'
        else:
            return 'ham'


    def evaluate(self, test_filename):
        TP = 0
        FP = 0
        FN = 0
        TN = 0
        with open(test_filename,'r') as f:
            for line in f:
                line = line.strip()
                label = line.split('\t')[0]
                text = line.split('\t')[1]


                if (self.predict(text) == 'spam' and label == 'spam'):
                    TP = TP + 1
                elif (self.predict(text) == 'ham' and label == 'ham'):
                    TN = TN + 1
                elif (self.predict(text) == 'ham' and label == 'spam'):
                    FN = FN + 1
                elif (self.predict(text) == 'spam' and label == 'ham'):
                    FP = FP + 1

        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        fscore = 2 * precision * recall / (precision + recall)
        accuracy = (TP + TN) / (TP + TN + FN + FP)
        return precision, recall, fscore, accuracy



def print_result(result):
    print("Precision:{} Recall:{} F-Score:{} Accuracy:{}".format(*result))


if __name__ == "__main__":

    classifier = NbClassifier(sys.argv[1],sys.argv[3])
    result = classifier.evaluate(sys.argv[2])
    print_result(result)
