import os
import json
import re

from collections import OrderedDict

from bs4 import BeautifulSoup
from hyphen import Hyphenator, dictools

from flask import current_app

if not dictools.is_installed("ru_RU"):
    dictools.install("ru_RU")

RU_HYPHENATOR = Hyphenator("ru_RU")
SOFT_HYPHEN = u"\u00AD"
STRIP_WHITESPACE = re.compile("\w+", re.MULTILINE | re.UNICODE)
HYPHENATOR_BLACKLIST_TAGS = ("code", "tt", "pre", "head", "title", "script", "style", "meta", "object", "embed",
                             "samp", "var", "math", "select", "option", "input", "textarea", "span", "iframe")


def no_shy(text):
    return text.replace(SOFT_HYPHEN, "")


def get_data(module):
    index_path = os.path.join(current_app.root_path, "data", module, "posts.json")

    with open(index_path, "r", encoding="utf8") as index_file:
        return OrderedDict([(p[0], p) for p in json.load(index_file)])


def get_content(module, file_name):
    file_path = os.path.join(current_app.root_path, "data", module, file_name.split("_")[0], file_name)

    with open(file_path, "r", encoding="utf8") as file_handler:
        return file_handler.read()


def hyphenate_word(word):
    syllables = RU_HYPHENATOR.syllables(word)

    return SOFT_HYPHEN.join(syllables) if syllables else word


def hyphenate(html):
    soup = BeautifulSoup(html, "html.parser")

    for paragraph in soup.findAll(text=lambda text: len(text)):
        if paragraph.parent.name in HYPHENATOR_BLACKLIST_TAGS:
            continue

        paragraph.replaceWith(STRIP_WHITESPACE.sub(
            (lambda x: hyphenate_word(x.group())), paragraph)
        )

    return soup
