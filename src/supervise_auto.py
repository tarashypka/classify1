import json
import os
import sys

from utils import paths


def read_label_for(text):
    print(text)
    label = input('Enter class label (0 rom, 1 eng, 2 skip, 3 save): ')
    try:
        label = int(label)
    except Exception:
        label = read_label()
    return label


def close_and_exit():
    print('Closing files to prevent data loss ...')
    fr.close()
    fw.close()
    sys.exit(1)


if __name__ == '__main__':
    read_f = paths.test.TEXTS_JSON
    write_f = paths.test.TEXTS_LABELED_JSON
    with open(read_f) as fr, open(write_f, 'a') as fw:
        for i, line in enumerate(fr, start=1):
            os.system('clear')
            print('document', i)
            try:
                doc = json.loads(line)
                label = read_label_for(text=doc['text'])
                if label == 0 or label == 1:
                    doc['class_true'] = label
                    text = json.dumps(doc, ensure_ascii=False, sort_keys=True)
                    fw.write(text + '\n')
                elif label == 3:
                    close_and_exit()
            except Exception as ex:
                print(ex)
                close_and_exit()
