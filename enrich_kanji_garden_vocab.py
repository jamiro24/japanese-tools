import pandas as pd
import os
from tkinter import filedialog
import tkinter as tk

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.withdraw()

print("Please select the kanji garden vocab file \n")

file_path = filedialog.askopenfilename(initialdir=ROOT_DIR)
output_path = filedialog.asksaveasfilename(initialdir=ROOT_DIR)

df = pd.read_csv(file_path, sep="\t")

del df["pos"]

# -*- coding:utf-8 -*-
ranges = [
  {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
  {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
]


def is_kana(char):
  return any([range["from"] <= ord(char) <= range["to"] for range in ranges])


def create_furigana(x: str) -> str:
    (word, reading) = x.split("***")
    reading = reading.split("・")[0].strip()
    full_reading = ""
    r_parts = reading.split(".")
    index = 0
    for symbol in word:
        if is_kana(symbol):
            full_reading += symbol
            r_parts[index] = r_parts[index][1:]
            if r_parts[index] == "":
                index += 1
        else:
            full_reading += f'{symbol}[{r_parts[index]}]'
            index += 1

    return full_reading


df["meaning"] = df["meaning"].apply(lambda x: x.replace("・", ", ").replace(";", ", "))
df["full reading"] = (df['word'] + "***" + df['reading']).apply(create_furigana)
df["alternative meanings"] = df["meaning"].apply(lambda x: ", ".join(x.split(", ")[1::]))
df["meaning"] = df["meaning"].apply(lambda x: x.split(", ")[0])
df["reading"] = df["reading"].apply(lambda x: x.split("・*")[0].replace(".", ""))

df["alternative reading"] = ""
duplicates = df[df["word"].duplicated() == True]
df = df.drop_duplicates(subset=["word"])
for i, row in duplicates.iterrows():
    word = row["word"]
    reading = row["reading"]
    df.loc[df["word"] == word, "alternative reading"] += reading

df = df[["word", "reading", "alternative reading", "full reading", "meaning", "alternative meanings"]]
df.to_csv(output_path, sep="\t")


