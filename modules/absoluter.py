from markdown.treeprocessors import Treeprocessor
from markdown import Extension

from urlparse import urljoin, urlparse

import flask

class AbsoluterExtension(Extension):
    def __init__(self, base_url):
        self.base_url = base_url

    def extendMarkdown(self, md, md_globals):
        absoluter = AbsoluterTreeprocessor(md)

        absoluter.config = {
            "base_url": self.base_url
        }

        md.treeprocessors.add("absoluter", absoluter, "_end")
        md.registerExtension(self)

class AbsoluterTreeprocessor(Treeprocessor):
    def run(self, root):
        first_image = None

        base_url = self.config["base_url"]()

        imgs = root.getiterator("img")

        for image in imgs:
            image.set("itemprop", "image")

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

def makeExtension(base_url):
    return AbsoluterExtension(base_url)