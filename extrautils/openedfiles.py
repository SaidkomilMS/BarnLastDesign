import json
import sys
import os


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


with open(r"statics\style.css", "rt") as css_file:
    css_style: str = css_file.read()

with open(r"jdata\weekend.json", 'rt') as jfile:
    week_lim: int = json.load(jfile)
