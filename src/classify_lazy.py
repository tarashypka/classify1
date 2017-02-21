import json
import random
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import stopwords

from utils import paths
from utils import read_test_labels
from utils import write_train_labels
from preprocess import replace_special


stop_rom = set(stopwords.words('romanian'))
stop_rom = set(replace_special(' '.join(stop_rom)).split())
stop_eng = set(stopwords.words('english'))

# Common stopwords
stop_rom_eng = stop_rom.intersection(stop_eng)
stop_eng_in_rom = set(['in', 'o', 'a'])
stop_rom_in_eng = set([])

# Prepare stopwords
stop_rom -= stop_rom_eng
stop_eng -= stop_rom_eng
stop_eng -= stop_eng_in_rom
stop_rom -= stop_rom_in_eng

ROM_LABEL = 0
ENG_LABEL = 1


def d(x1, x2):
    """
    Distance metric of whether the text was badly recognized.
    Takes into accont both distance from the line x1=x2
    and total # of stopwords x1+x2.

    Parameters
    ----------
    x1 : int
        # of X-language stopwords in some text T
    x2 : int
        # of Y-language stopwords in some text T

    Returns
    -------
    float
        Distance estimation.
    """
    return abs(x1-x2) / ((x1 + x2 + 1) * sqrt(2))


# Texts with dist < DIST_THRESHOLD  are hard to recognize
DIST_THRESHOLD = 0.35


def read_dataset(read_f):
    X = []
    with open(read_f, 'r') as f:
        for line in f:
            skip = False
            try:
                doc = json.loads(line)
            except JSONDecodeError:
                continue
            else:
                try:
                    text = doc['text']
                except KeyError:
                    continue
            terms = text.lower().split()
            x1 = len([term for term in terms if term in stop_rom])
            x2 = len([term for term in terms if term in stop_eng])
            dist = d(x1, x2)
            X.append([x1, x2, dist])
    return np.asarray(X)


def compute_accuracy():
    X = read_dataset(paths.test.TEXTS_LABELED_JSON)
    y_predicted = np.zeros(len(X))
    y_predicted[np.where(X[:, 1] > X[:, 0])] = ENG_LABEL
    y_target = read_test_labels()
    texts = [json.loads(line)['text']
             for line in open(paths.test.TEXTS_LABELED_JSON)]
    misclassified = np.where(y_predicted != y_target)[0]

    # Show random 10 misclassified samples
    for wrong in random.sample(list(misclassified), 10):
        print('Misclassified sample (%s) with %s rom, %s eng stopwords:\n%s' %
              (wrong, int(X[wrong, 0]), int(X[wrong, 1]), texts[wrong]))

    accuracy = 1 - len(misclassified) / len(y_target)
    return accuracy


if __name__ == '__main__':
    X = read_dataset(paths.train.TEXTS_JSON)
    hard = X[:, 2] < DIST_THRESHOLD
    X_hard = X[hard][:, [0, 1]]
    empty = (X_hard[:, 1] == 0) * (X_hard[:, 1] == 0)
    X_empty = X_hard[empty][:, [0, 1]]
    X_easy = X[~hard][:, [0, 1]]
    print('There are %s texts wout stopwords' % len(X_empty))
    plt.scatter(X_hard[:, 0], X_hard[:, 1], s=0.2,
                color='red', label='hard stopwords (%s)' % len(X_hard))
    plt.scatter(X_easy[:, 0], X_easy[:, 1], s=0.2,
                color='green', label='easy stopwords (%s)' % len(X_easy))
    plt.plot([0, max(X[:, 0])], [0, max(X[:, 1])],
             color='black', label='decision boundary')
    plt.xlabel('rom stopwords #')
    plt.ylabel('eng stopwords #')
    plt.legend()
    plt.show()

    # Performance on test set to compare
    print('Accuracy', compute_accuracy())
