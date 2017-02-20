import json
import os

import numpy as np


class paths:
    DATA_PATH = os.getenv('PROJPATH') + '/data'
    TEXTS_RAW_JSON = DATA_PATH  + '/raw_text_ro.json'
    TEXTS_JSON = DATA_PATH + '/text_ro.json'
    TEXTS_TXT = DATA_PATH + '/text_ro.txt'
    TERMS_DICT = DATA_PATH + '/terms_ro.dict'

    class train:
        TRAIN_PATH = os.getenv('PROJPATH') + '/data/train'
        TEXTS_JSON = TRAIN_PATH + '/text_ro.json'
        TEXTS_TXT = TRAIN_PATH + '/text_ro.txt'
        TERMS_CORP = TRAIN_PATH + '/terms_ro.mm'

    class test:
        TEST_PATH = os.getenv('PROJPATH') + '/data/test'
        TEXTS_JSON = TEST_PATH + '/text_ro.json'
        TEXTS_LABELED_JSON = TEST_PATH + '/text_labeled_ro.json'
        TEXTS_TXT = TEST_PATH + '/text_ro.txt'
        TEXTS_LABELED_TXT = TEST_PATH + '/text_labeled_ro.txt'
        TERMS_CORP = TEST_PATH + '/terms_ro.mm'


def read_labels():
    y_target = []
    with open(paths.test.TEXTS_LABELED_JSON) as f:
        for line in f:
            doc = json.loads(line)
            y_target.append(doc['class'])
    return np.asarray(y_target)
