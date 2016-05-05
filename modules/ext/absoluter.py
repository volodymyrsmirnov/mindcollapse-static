from urllib.parse import urljoin, urlparse

from markdown.treeprocessors import Treeprocessor
from markdown import Extension


class AbsoluterExtension(Extension):
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

        # noinspection PyUnresolvedReferences
        base_url = self.config.get("base_url")()

        for image in root.getiterator("img"):
            image.set("itemprop", "image")

            if urlparse(image.attrib.get("src")).scheme == "":
                image.set("src", urljoin(base_url, image.attrib.get("src")))

            if not first_image:
                first_image = image.attrib.get("src")

        self.markdown.first_image = first_image

        for link in root.getiterator("a"):
            parsed_link = urlparse(link.attrib.get("href"))

            if not parsed_link.scheme and not parsed_link.netloc and parsed_link.path:
                link.set("href", urljoin(base_url, link.attrib.get("href")))

            elif parsed_link.netloc and parsed_link.netloc not in base_url:
                link.set("rel", "nofollow")
                link.set("target", "_blank")


# noinspection PyPep8Naming
def makeExtension(base_url):
    return AbsoluterExtension(base_url)
