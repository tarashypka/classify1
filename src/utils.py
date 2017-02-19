from math import floor

import os
import json
import random
from json.decoder import JSONDecodeError


class paths:
    PROJPATH = os.getenv('PROJPATH')
    TEXTS_RAW_JSON = PROJPATH + '/data/raw_text_ro.json'
    TEXTS_TXT = PROJPATH + '/data/text_ro.txt'
    TERMS_DICT = PROJPATH + '/data/terms_ro.dict'
    TERMS_CORP = PROJPATH + '/data/terms_ro.mm'
