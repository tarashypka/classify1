import json
import random
from math import floor

import numpy as np
from gensim import corpora
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
from sklearn.model_selection import train_test_split

from utils import paths
from utils import read_test_labels
from utils import write_train_labels


method = 'km'
CLASSIFIERS = {
    'km': KMeans(n_clusters=2,
                 init='k-means++',
                 n_init=10,
                 max_iter=300,
                 tol=1e-04,
                 random_state=0,
                 n_jobs=4),
}
DATASET_SIZE = 1.0
CV_SIZE = 0.3
ROM_LABEL = 0
ENG_LABEL = 1


def normalize(X):
    """
    Modify each input example with new counts, so that
    term_1_count + term2_count + ... + termN_count = 1.
    This will allow not to take into account the initial document length.
    """
    return X / (1 + np.sum(X, axis=1)[:, None])


def get_data(corpus, n_features):
    print(len(corpus), 'samples,', n_features, 'features')
    X = []
    for doc in corpus:
        x = [0] * n_features
        for term_id, term_freq in doc:
            x[term_id] = term_freq
        X.append(x)
    X = np.asarray(X)
    X = X[:floor(DATASET_SIZE * len(X))]
    X = normalize(X)
    return X


def compute_accuracy(classifier, dict_):
    # Load test dataset
    corpus = list(corpora.MmCorpus(paths.test.TERMS_CORP))
    X_test = get_data(corpus, n_features=len(dict_))
    y_predicted = classifier.predict(X_test)
    y_target = read_test_labels()
    texts = [json.loads(line)['text']
             for line in open(paths.test.TEXTS_LABELED_JSON)]

    # Show classified examples with predicted labels
    terms = np.asarray(list(dict_.values()))
    for xi, yi in zip(X_test[:25], y_predicted[:25]):
        xterms = xi.nonzero()
        print('Prediction:', yi, 'for terms', terms[xterms])

    # Select correct label for romanian language
    rom_label = int(input('Enter label for romanian language: '))
    if rom_label != ROM_LABEL:
        y_target = 1 - y_target  # swap labels
    eng_ix = np.where(y_target == 0)[0]

    misclassified = np.where(y_predicted != y_target)[0]
    # Show random 10 misclassified samples
    for wrong in random.sample(list(misclassified), 10):
        print('Misclassified sample:', texts[wrong])

    accuracy = 1 - len(misclassified) / len(y_target)
    return accuracy


if __name__ == '__main__':
    dict_ = corpora.Dictionary.load(paths.TERMS_DICT)
    corpus = list(corpora.MmCorpus(paths.train.TERMS_CORP))
    X = get_data(corpus, n_features=len(dict_))
    X_train, X_cv =  train_test_split(X, test_size=CV_SIZE, random_state=0)

    print('Training...')
    classifier = CLASSIFIERS[method]
    classifier = classifier.fit(X_train)
    y_train = classifier.predict(X_train)
    y_cv = classifier.predict(X_cv)

    # Save train sample predicted results
    #y_train = classifier.predict(X)
    #write_f = paths.train.TRAIN_PATH + '/text_kmeans_ro.json'
    #write_train_labels(write_f, y_train)

    # Performance on CV set to tune model parameters
    #print(metrics.silhouette_score(X_cv, y_cv, metric='euclidean'))
    #print(metrics.calinski_harabaz_score(X_cv, y_cv))

    # Performance on test set to estimate model
    print('Accuracy', compute_accuracy(classifier, dict_))
