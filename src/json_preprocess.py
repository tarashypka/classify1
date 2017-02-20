import json
from json.decoder import JSONDecodeError

from utils import paths


def preprocess(read_f, write_f):
    """
    Remove redundant fields (id).
    Merge title and text fields into single text field.
    Add class label field with default value 0.
    """
    with open(read_f) as fr, open(write_f, 'w') as fw:
        #non_ascii = set()
        for line in fr:
            try:
                doc = json.loads(line)
            except JSONDecodeError:
                continue
            else:
                try:
                    del doc['id']
                    doc['class'] = '0'
                    doc['text'] = doc['title'] + ' ' + doc['text']
                    del doc['title']
                except KeyError:
                    continue
            text = json.dumps(doc, ensure_ascii=False, sort_keys=True)
            #non_ascii |= set([c for c in text if ord(c) >= 128])
            fw.write(text + '\n')


if __name__ == '__main__':
    preprocess(paths.TEXTS_RAW_JSON, paths.TEXTS_JSON)
