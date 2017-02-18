from math import floor

import os
import json
import random
from json.decoder import JSONDecodeError


JSON_TEXT_PATH = os.getenv('PROJPATH') + '/data/raw_text_ro.json'
JSON_TERMS_PATH = os.getenv('PROJPATH') + '/data/terms_ro.json'


def _read_docs(path, fields, max_docs, max_docs_pers, random_docs):
    """
    Retrieve reduced documents from json.

    Parameters
    ----------
    path : str
        Absolute path to the json file.
    fields : [str]
        Fields names to retrieve.
    max_docs : int
        Maximum # of documents to look at. Defaults to all docs in the file.
        For simplicity sake, docs with decode errors will be skipped.
        If not supplied, then all documents will be parsed.
    max_docs_pers : float
        Maximum % of documents to look at.
    random_docs : bool
        Has no effect if max_docs is None.

    Returns
    -------
    list
        List with all documents having specified fields.
    """
    docs = open(path).read().splitlines()
    n_docs = len(docs)
    if max_docs:
        n_docs = max_docs
    elif max_docs_pers:
        n_docs = floor(max_docs_pers * n_docs)
    docs = random.sample(docs, n_docs) if random_docs else docs[:n_docs]
    json_docs = [] 
    for doc in docs:
        jdoc = {}
        skip = False
        try:
            doc = json.loads(doc)
        except JSONDecodeError:
            skip = True
        else:
            for field in fields:
                try:
                    jdoc[field] = doc[field]
                except KeyError:
                    skip = True
                    break
        finally:
            if not skip:
                json_docs.append(jdoc)
    return json_docs


def read_text(*, path=JSON_TEXT_PATH, fields=None, max_docs=None,
              max_docs_pers=None, random_docs=False):

    """
    Read raw text documents from the file.
    """
    all_fields = ['id', 'title', 'text']
    if not fields:
        fields = all_fields
    return _read_docs(path, fields, max_docs, max_docs_pers, random_docs)


def read_terms(*, path=JSON_TERMS_PATH, fields=None, max_docs=None,
               max_docs_pers=None, random_docs=False):

    """
    Read terms json documents from the file.
    """
    all_fields = ['id', 'terms']
    if not fields:
        fields = all_fields
    return _read_docs(path, fields, max_docs, max_docs_pers, random_docs)


def _write_docs(docs, path):
    """
    Write json documents to the file line-by-line.
    """
    with open(path, 'w') as f:
        for doc in docs:
            json.dump(doc, f, ensure_ascii=False)
            f.write('\n')


def write_terms(terms, *, path=JSON_TERMS_PATH):
    """
    Write terms json documents to the file.
    """
    _write_docs(terms, path)
