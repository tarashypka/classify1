import json
import sys

from utils import paths


def read_label():
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
        for line in fr:
            try:
                doc = json.loads(line)
                print(doc['text'])
                label = read_label()
                if label == 0 or label == 1:
                    doc['class'] = label
                    text = json.dumps(doc, ensure_ascii=False, sort_keys=True)
                    fw.write(text + '\n')
                elif label == 3:
                    close_and_exit()
                # Delete line ?
            except Exception as ex:
                print(ex)
                close_and_exit()
