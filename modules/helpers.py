import os
import json
import re

from collections import OrderedDict

from hyphenator import Hyphenator
from BeautifulSoup import BeautifulSoup

import flask 

def no_shy(text):
    return text.replace(u"\u00AD", "")

def get_data(module):
    index_path = os.path.join(flask.current_app.root_path, "data", module, ".index")

    data_list = []

    with open(index_path, "rb") as index_file:
        for post in json.loads(index_file.read()):
            data_list.append((post[0], post))

    return OrderedDict(data_list)

def get_content(module, contentfile):
    year = contentfile.split("_")[0]
    
    file_path = os.path.join(flask.current_app.root_path, "data", module, year, contentfile)

    try:
        with open(file_path, "r") as file_handler:
            return unicode(file_handler.read().decode("utf-8"))
    except IOError:
        return ""

def hyphenate(html, hyphenator=None, blacklist_tags=(
        "code", "tt", "pre", "head", "title", "script", "style", "meta", "object",
        "embed", "samp", "var", "math", "select", "option", "input", "textarea",
        "span",
    )):

    if not hyphenator:
        hyphenator = Hyphenator(os.path.join(flask.current_app.root_path, "data", "hyphenation.dic"))

    soup = BeautifulSoup(html)

    hyphenate_element(soup, hyphenator, blacklist_tags)

    return unicode(soup)

SOFT_HYPHEN = u'\u00AD'
STRIP_WHITESPACE = re.compile('\w+', re.MULTILINE|re.UNICODE)

def hyphenate_element(soup, hyphenator, blacklist_tags):
    BLACKLIST = lambda tag: tag in blacklist_tags
    
    paragraphs = soup.findAll(text = lambda text: len(text) > 0)
    for paragraph in paragraphs:
        if not BLACKLIST(paragraph.parent.name):
            paragraph.replaceWith(STRIP_WHITESPACE.sub(
                (lambda x: hyphenator.inserted(x.group(), SOFT_HYPHEN)), paragraph)
            )

    return soup