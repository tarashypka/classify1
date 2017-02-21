import json
import os

import numpy as np


class paths:
    DATA_PATH = os.getenv('PROJPATH') + '/data'
    TEXTS_RAW_JSON = DATA_PATH  + '/raw_text_ro.json'
    TEXTS_JSON = DATA_PATH + '/text_ro.json'
    TERMS_DICT = DATA_PATH + '/terms_ro.dict'

    class train:
        TRAIN_PATH = os.getenv('PROJPATH') + '/data/train'
        TEXTS_JSON = TRAIN_PATH + '/text_ro.json'
        TERMS_CORP = TRAIN_PATH + '/terms_ro.mm'

        TEXTS_JSON_OUTP = TRAIN_PATH + '/text_outp_ro.json'

    class test:
        TEST_PATH = os.getenv('PROJPATH') + '/data/test'
        TEXTS_JSON = TEST_PATH + '/text_ro.json'
        TEXTS_LABELED_JSON = TEST_PATH + '/text_labeled_ro.json'
        TERMS_CORP = TEST_PATH + '/terms_ro.mm'


def read_test_labels():
    y_target = []
    with open(paths.test.TEXTS_LABELED_JSON) as f:
        for line in f:
            doc = json.loads(line)
            y_target.append(doc['class_true'])
    return np.asarray(y_target)


def write_train_labels(write_f, labels):
    read_f = paths.train.TEXTS_JSON
    n_labels = len(labels)
    with open(read_f) as fr, open(write_f, 'w') as fw:
        for i, line in enumerate(fr):
            if i > n_labels:
                break
            doc = json.loads(line)
            doc['class_pred'] = int(labels[i])
            text = json.dumps(doc, ensure_ascii=False, sort_keys=True)
            fw.write(text + '\n')
