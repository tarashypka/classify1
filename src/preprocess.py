import sys
import json
from json.decoder import JSONDecodeError

import regex as re

from utils import paths


# Handle special characters, numbers, punctuation
PATTERN_NUMBERS = [r'(\d)+', ' ']
PATTERN_PUNCTUATION = [r'\p{P}+', ' ']
PATTERN_NOTERM = [r'\+|●|\$|€|\£||||\|', ' ']
SPECIAL = 'ĂăÂâÎîȘșŞşȚțŢţ'
PATTERN_SPECIAL = [r'\w*(' + '|'.join(SPECIAL) + r')\w*', 'ROM_SPECIAL']

# Both in romanian and english languages
stopterms = set(['a', 'an', 'in'])


def replace_special(text):
    return re.sub(PATTERN_SPECIAL[0], PATTERN_SPECIAL[1], text)


def preprocess(text):
    """
    Remove numbers, punctuation, redundant whitespaces, special signs,
    stopterms. Replaces special romanian characters with ROM_SPECIAL.
    """
    text = text.lower()
    text = re.sub(PATTERN_NUMBERS[0], PATTERN_NUMBERS[1], text)
    text = re.sub(PATTERN_PUNCTUATION[0], PATTERN_PUNCTUATION[1], text)
    text = re.sub(PATTERN_NOTERM[0], PATTERN_NOTERM[1], text)
    text = replace_special(text)
    terms = text.split()
    terms = [term for term in terms if term not in stopterms]
    text = ' '.join(terms)
    return text


def preprocess_and_write(read_f, write_f):
    """
    Merge title and text fields into single text field.
    Preprocess text.
    """
    with open(read_f) as fr, open(write_f, 'w') as fw:
        for line in fr:
            try:
                doc = json.loads(line)
            except JSONDecodeError:
                continue
            else:
                try:
                    text = doc['title'] + ' ' + doc['text']
                    text = preprocess(text)
                    doc['text'] = text
                    del doc['title']
                except KeyError:
                    continue
            text = json.dumps(doc, ensure_ascii=False, sort_keys=True)
            fw.write(text + '\n')


if __name__ == '__main__':
    preprocess_and_write(paths.TEXTS_RAW_JSON, paths.TEXTS_JSON)
