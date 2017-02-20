import sys
import json

import regex as re

from utils import paths


# Handle special characters, numbers, punctuation
PATTERN_NUMBERS = [r'(\d)+', ' ']
PATTERN_PUNCTUATION = [r'\p{P}+', ' ']
PATTERN_NOTERM = [r'\+|\$|€|||\|', ' ']
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


def process_and_write(read_f, write_f):
    with open(read_f) as fr, open(write_f, 'w') as fw:
        for line in fr:
            skip = False
            try:
                doc = json.loads(line)
            except JSONDecodeError:
                continue
            else:
                try:
                    text = doc['text']
                except KeyError:
                    continue
            text = preprocess(text)
            fw.write(text + '\n')


if __name__ == '__main__':
    process_and_write(paths.train.TEXTS_JSON, paths.train.TEXTS_TXT)
    process_and_write(paths.test.TEXTS_LABELED_JSON, paths.test.TEXTS_LABELED_TXT)
