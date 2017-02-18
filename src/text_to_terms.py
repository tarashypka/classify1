import regex as re
#from nltk import PorterStemmer
#from nltk.stem.snowball import RomanianStemmer

from utils import read_text
from utils import read_terms
from utils import write_terms


# To remove punctuation and numbers
PATTERN_NUMBERS = [r'[xX\s]*(\d+)[xX\s]*', r' \1 ']
PATTERN_PUNCTUATION = [r'\p{P}+', r' ']

# To remove short terms
TERM_MIN_LEN = 2


if __name__ == '__main__':
    docs = read_text()
    for doc in docs:
        text = doc['title'] + ' ' + doc['text']
        del doc['title']
        del doc['text']

        # Remove punctuation and numbers
        text = re.sub(PATTERN_PUNCTUATION[0], PATTERN_PUNCTUATION[1], text)
        text = re.sub(PATTERN_NUMBERS[0], PATTERN_NUMBERS[1], text)

        terms = text.split()

        # Perform stemming
        #terms = [PorterStemmer().stem(term) for term in terms]
        #terms = [RomanianStemmer().stem(term) for term in terms]

        # Remove short terms
        terms = [term for term in terms if len(term) >= TERM_MIN_LEN]
        doc['terms'] = terms

    write_terms(docs)
    terms = read_terms()
    print(len(terms))
