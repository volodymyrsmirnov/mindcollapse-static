from markdown.treeprocessors import Treeprocessor
from markdown import Extension

from urlparse import urljoin, urlparse

import flask

class AbsoluterExtension(Extension):
    def __init__(self, configs=[]):
        self.config = {
            'base_url': [None, "Base URL"],
        }

        for key, value in configs:
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        absoluter = AbsoluterTreeprocessor(md)
        absoluter.config = self.getConfigs()
        md.treeprocessors.add("absoluter", absoluter, "_end")
        md.registerExtension(self)

class AbsoluterTreeprocessor(Treeprocessor):
    def run(self, root):
        first_image = None

        imgs = root.getiterator("img")

        for image in imgs:
            if urlparse(image.attrib["src"]).scheme == "":
                image.set("src", urljoin(self.config["base_url"](), image.attrib["src"]))

            if not first_image:
                first_image = image.attrib["src"]

        self.markdown.first_image = first_image

def makeExtension(configs=[]):
    return AbsoluterExtension(configs=configs)