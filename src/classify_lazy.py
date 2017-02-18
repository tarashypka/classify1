import json
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np

from utils import read_terms
from stopwords import stop_rom
from stopwords import stop_eng


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


if __name__ == '__main__':
    docs = read_terms()

    # Prepare dataset
    X = np.empty((0, 3), int)
    for i, doc in enumerate(docs, start=1):
        terms = doc['terms']
        stop_rom_ = [term for term in terms if term in stop_rom]
        stop_eng_ = [term for term in terms if term in stop_eng]
        x1, x2 = len(stop_rom_), len(stop_eng_)
        dist = d(x1, x2)
        X = np.append(X, np.asarray([[x1, x2, dist]]), axis=0)
        # numpy solution of appending to the array is much faster than
        # pandas solution of appending to the dataframe

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
