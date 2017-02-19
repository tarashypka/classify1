import json

import regex as re
from nltk.corpus import stopwords

from utils import paths


# Handle special characters, numbers, punctuation
PATTERN_NUMBERS = [r'(\d)+', ' ']
PATTERN_PUNCTUATION = [r'\p{P}+', ' ']
PATTERN_NOTERM = [r'\+|\$', ' ']
SPECIAL = {
    'ă': 'a',
    'î': 'i',
    'ș': 's',
    'ț': 't',
    'ţ': 't',
    'é': 'e'
}
PATTERN_SPECIAL = re.compile(r'(' + '|'.join(SPECIAL.keys()) + r')')

TERM_LEN_MIN = 3

stop_terms = set(stopwords.words('romanian'))
stop_terms |= set(stopwords.words('english'))
# Stopwords that appear both in romanian and english
with open('data/stopwords/rom_in_eng', 'r') as f:
    stop_terms |= set(f.read().splitlines())


def preprocess(text):
    """
    Remove numbers, punctuation, redundant whitespaces, special signs.
    Eliminate stopwords: both self-constructed and public.
    Remove terms that are too short.
    Replaces special romanian characters with common.
    """
    text = text.lower()
    text = re.sub(PATTERN_NUMBERS[0], PATTERN_NUMBERS[1], text)
    text = re.sub(PATTERN_PUNCTUATION[0], PATTERN_PUNCTUATION[1], text)
    text = re.sub(PATTERN_NOTERM[0], PATTERN_NOTERM[1], text)
    terms = [term for term in text.split() if len(term) >= TERM_LEN_MIN]
    terms = [term for term in terms if term not in stop_terms]
    text = ' '.join(terms)
    text = PATTERN_SPECIAL.sub(lambda x: SPECIAL[x.group()], text)
    return text


if __name__ == '__main__':
    with open(paths.TEXTS_RAW_JSON) as fr, open(paths.TEXTS_TXT, 'w') as fw:

        for line in fr:
            skip = False
            try:
                doc = json.loads(line)
            except JSONDecodeError:
                skip = True
            else:
                try:
                    text = doc['title'] + ' ' + doc['text']
                except KeyError:
                    skip = True
            finally:
                if not skip:
                    text = preprocess(text)
                    fw.write(text + '\n')
