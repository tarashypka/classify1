from gensim import corpora
from six import iteritems

from nltk.corpus import stopwords
from utils import paths


TERM_FREQ_MIN = 1000


if __name__ == '__main__':
    # Loaded text is already preprocessed
    dict_ = corpora.Dictionary(line.split() for line in open(paths.TEXTS_TXT))
    rare_ids = \
        [id_ for id_, freq in iteritems(dict_.dfs) if freq < TERM_FREQ_MIN]
    dict_.filter_tokens(rare_ids)
    dict_.compactify()
    dict_.save(paths.TERMS_DICT)
    corpus = [dict_.doc2bow(line.split()) for line in open(paths.TEXTS_TXT)]
    corpora.MmCorpus.serialize(paths.TERMS_CORP, corpus)
