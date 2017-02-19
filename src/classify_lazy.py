import json
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import stopwords

from utils import paths


stop_rom = set(stopwords.words('romanian'))
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


def read_dataset():
    X = []
    with open(paths.TEXTS_RAW_JSON, 'r') as f:
        for line in f:
            skip = False
            try:
                doc = json.loads(line)
            except JSONDecodeError:
                skip = True
            else:
                try:
                    text = doc['title'] + ' ' + doc['text']
                except KeyError:
                    skip = True
            finally:
                if not skip:
                    terms = text.lower().split()
                    x1 = len([term for term in terms if term in stop_rom])
                    x2 = len([term for term in terms if term in stop_eng])
                    dist = d(x1, x2)
                    X.append([x1, x2, dist])
    return np.asarray(X)


if __name__ == '__main__':
    X = read_dataset()
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
