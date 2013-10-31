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

        base_url = self.config["base_url"]()

        imgs = root.getiterator("img")

        for image in imgs:
            if urlparse(image.attrib["src"]).scheme == "":
                image.set("src", urljoin(base_url, image.attrib["src"]))

            if not first_image:
                first_image = image.attrib["src"]

        self.markdown.first_image = first_image

        links = root.getiterator("a")

        for link in links:
            parsed_link = urlparse(link.attrib["href"])

            if not parsed_link.scheme and not parsed_link.netloc and parsed_link.path:
                link.set("href", urljoin(base_url, link.attrib["href"]))
            elif parsed_link.netloc and parsed_link.netloc not in base_url:
                link.set("rel", "nofollow")

def makeExtension(configs=[]):
    return AbsoluterExtension(configs=configs)