import os
import re
import requests
import csv
import time
import tkinter as tk
from tkinter import filedialog
from collections import OrderedDict


def is_kanji(texts):
    if re.search("[\u4e00-\u9FFF]", texts):
        return True
    return False


def get_unique_kanji(file_content):
    characters = OrderedDict()
    for line in file_content:
        for character in line:
            kanji = is_kanji(character)
            if kanji:
                characters[character] = True
    return [c for c, d in characters.items()]


def get_kanji_info(kanji):
    url = f"https://kanjiapi.dev/v1/kanji/{kanji}"
    result = requests.get(url)
    return result.json()


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(initialdir=ROOT_DIR)

# noinspection PyBroadException
try:
    with open(file_path, encoding="utf8") as f:
        with open(f'{ROOT_DIR}/output.tsv', "wt", encoding="utf8") as tsvout:
            writer = csv.writer(tsvout, delimiter="\t")
            unique_kanji = get_unique_kanji(f)
            counter = 0
            for char in unique_kanji:
                counter += 1
                print(f"processing {counter}/{len(unique_kanji)} ({char})")
                info = get_kanji_info(char)
                line_out = [
                    info["kanji"],
                    info["grade"],
                    info["jlpt"],
                    info["stroke_count"],
                    ", ".join(info["meanings"]),
                    ", ".join(info["on_readings"]) if len(info["on_readings"]) > 0 else " ",
                    ", ".join(info["kun_readings"]) if len(info["kun_readings"]) > 0 else " ",
                ]
                writer.writerow(line_out)
except FileNotFoundError as e:
    print(e)
    exit(0)
except Exception as e:
    print("Kanji info could not be obtained, you are probably making too many requests or have lost your internet "
          "connection")
    print("Try again later with a file with less unique kanji")
    time.sleep(5)
    exit(0)

