import csv

import os
from os import listdir
from os.path import isfile, join

hiragana = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりろれろわを".split()
katakana = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲ".split()


def create_reading(str):
    intermediate = str
    for elem in hiragana + katakana:
        intermediate = str.replace(elem, ",")
    kanji_segments = intermediate.split(",")
    kanji_segments = [elem for elem in kanji_segments if elem != ""]
    print([elem.encode() for elem in kanji_segments])


dir = os.path.dirname(os.path.abspath(__file__))
onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]

tsvs = [f for f in onlyfiles if f.endswith(".tsv") and f != "vocab.tsv"]

if len(tsvs) != 1:
    print("Please put (only) one '.tsv' file in this folder.")
    exit(0)


with open(f'{dir}/{tsvs[0]}', 'r', encoding="utf-8") as tsvin, open(f'{dir}/vocab.tsv', 'w', encoding="utf-8") as csvout:
    reader = csv.reader(tsvin, delimiter='\t')
    writer = csv.writer(csvout, delimiter='\t')

    # writer.writerow(["Kanji", "Reading", "English", "Alternative Meanings"])

    first = True

    for row in reader:
        if first:
            first = False
            continue
        create_reading(row[0])
        # meanings = row[3].replace("・", ";").split(";")
        # row[3] = meanings[0]
        # if len(meanings) > 1:
        #     row.append(", ".join(meanings[1:]))
        # else:
        #     row.append("")
        # del row[2]
        # row.append(row[0])
        # writer.writerow(row)



