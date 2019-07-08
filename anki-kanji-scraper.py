import os
import re
import requests
import csv
import time
import tkinter as tk
from tkinter import filedialog
from collections import OrderedDict
from colorama import Fore


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


def extract_info(info):
    return [
        info["kanji"],
        info["grade"],
        info["jlpt"],
        info["stroke_count"],
        ", ".join(info["meanings"]),
        ", ".join(info["on_readings"]) if len(info["on_readings"]) > 0 else " ",
        ", ".join(info["kun_readings"]) if len(info["kun_readings"]) > 0 else " ",
    ]


def get_custom_data():
    with_custom = input("Would you like to include custom fields?\n"
                        "To do this you require a '.csv' or '.tsv' file with at least a 'kanji' field and some other "
                        f"field.\ntype {Fore.CYAN}yes {Fore.YELLOW}and press enter{Fore.RESET} if you want this, otherwise just{Fore.YELLOW} "
                        f"press enter{Fore.RESET}.\n")

    if with_custom:
        print("Please select the '.csv' or '.tsv' file.")
        custom_csv = filedialog.askopenfilename(initialdir=ROOT_DIR)
        with open(custom_csv, encoding="utf-8") as custom:
            if custom_csv.endswith(".csv"):
                delimiter = ","
            elif custom_csv.endswith(".tsv"):
                delimiter = "\t"
            else:
                print("This file is not compatible, sorry!")
                exit(0)
            reader = csv.reader(custom, delimiter=delimiter)

            first_line = True
            field_kanji_index = None
            fields_custom_index = []
            data_custom = {}

            for line in reader:
                if first_line:
                    first_line = False

                    if len(line) < 2:
                        print("To add custom data there need to be at least 2 fields.")
                        time.sleep(5)
                        exit(0)

                    print(f"Found the following field: {', '.join(line)}\n")

                    while field_kanji_index is None:
                        try:
                            field_kanji_index = line.index(input("Type the name of the field that contains single "
                                                                 "kanji characters.\n"))
                        except:
                            print("This field does not exist")

                    while len(fields_custom_index) == 0:
                        fields_custom = [field.strip() for field in input("Type the names of the fields that you want "
                                                                          "to include as custom data\n").split(",")]
                        try:
                            fields_custom_index = [line.index(field) for field in fields_custom]
                        except:
                            print("Some of the fields you entered do not exist in the provided file.")
                else:
                    data_custom[line[field_kanji_index]] = [line[index] if len(line[index]) > 0 else " " for index in fields_custom_index]
            return data_custom
    else:
        return {}


def add_custom_data(char, line, data):
    key, value = list(data.items())[0]
    expected_length = len(value)
    new_data = data[char]
    while len(new_data) < expected_length:
        new_data += " "
    return line + new_data


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.withdraw()

print("Please select the file of which you want to extract kanji information.\n")

file_path = filedialog.askopenfilename(initialdir=ROOT_DIR)

custom_data = get_custom_data()

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
                line_out = extract_info(info)
                if len(custom_data) > 0:
                    line_out = add_custom_data(char, line_out, custom_data)
                writer.writerow(line_out)
except FileNotFoundError as e:
    print(e)
    exit(0)
except Exception as e:
    print("Kanji info could not be obtained, you are probably making too many requests, have lost your internet "
          "connection, or something else is wrong.\n"
          f"It could not be obtained due to the following reason: {e}")
    print("Try again later with a file with less unique kanji")
    time.sleep(5)
    exit(0)
