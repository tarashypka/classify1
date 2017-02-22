import json
from gensim import corpora
from six import iteritems

from utils import paths


TERM_LEN_MIN = 1
TERM_FREQ_MIN = 10000


def write_dict(read_f, write_f):
    dict_ = corpora.Dictionary(
        json.loads(line)['text'].split() for line in open(read_f))
    short_ids = \
        [id_ for id_, term in dict_.iteritems() if len(term) < TERM_LEN_MIN]
    rare_ids = \
        [id_ for id_, freq in iteritems(dict_.dfs) if freq < TERM_FREQ_MIN]
    dict_.filter_tokens(short_ids + rare_ids)
    dict_.compactify()
    dict_.save(write_f)
    return dict_


def write_corp(dict_, read_f, write_f):
    corpus = [dict_.doc2bow(
        json.loads(line)['text'].split()) for line in open(read_f)]
    corpora.MmCorpus.serialize(write_f, corpus)


# Loaded text is already preprocessed
if __name__ == '__main__':
    # Build terms dictionary from train set only
    dict_ = write_dict(paths.train.TEXTS_JSON, paths.TERMS_DICT)
    write_corp(dict_, paths.train.TEXTS_JSON, paths.train.TERMS_CORP)
    write_corp(dict_, paths.test.TEXTS_LABELED_JSON, paths.test.TERMS_CORP)
