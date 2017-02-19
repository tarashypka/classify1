from math import floor

import numpy as np
from gensim import corpora
from sklearn.cluster import KMeans

from utils import paths


if __name__ == '__main__':
    dict_ = corpora.Dictionary.load(paths.TERMS_DICT)
    terms = np.asarray(list(dict_.values()))
    corpus = list(corpora.MmCorpus(paths.TERMS_CORP))
    n_samples = floor(0.7 * len(corpus))
    n_features = len(dict_)
    print(n_samples, 'samples,', n_features, 'features')
    X = []
    for i, doc in enumerate(corpus[:n_samples]):
        x = [0] * n_features
        for term_id, term_freq in doc:
            x[term_id] = term_freq
        X.append(x)
    X = np.asarray(X)

    km = KMeans(n_clusters=2,
                init='k-means++',
                n_init=10,
                max_iter=300,
                tol=1e-04,
                random_state=0,
                n_jobs=4)

    print('Training...')
    y = km.fit_predict(X)
    for xi, yi in zip(X[:1000], y[:1000]):
        xterms = xi.nonzero()
        print('Prediction:', yi, 'for terms', terms[xterms])
    print('Inertia', km.inertia_)
