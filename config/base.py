import pytils
import os

from flask import url_for


class Config(object):
    DEBUG = True

    FREEZER_BASE_URL = "https://www.mindcollapse.com/"
    FREEZER_REMOVE_EXTRA_FILES = True
    FREEZER_DESTINATION = "build"
    FREEZER_DESTINATION_IGNORE = [
        ".git*",
        ".ht*",
        "robots.txt",
        "favicon.ico",
    ]

    PYSCSS_STATIC_ROOT = os.path.join(os.getcwd(), "static")
    PYSCSS_STATIC_URL = "/static"

    MD_OPTIONS = {
        "output_format": "html5",

        "extensions": [
            "toc",
            "extra",
            "smarty",
            "sane_lists",

            "modules.ext.absoluter",
        ],

        "extension_configs": {
            "toc": [
                ("anchorlink", True),
                ("slugify", lambda s, sep: pytils.translit.slugify(s)),
            ],

            "modules.ext.absoluter": [
                ("base_url", lambda: url_for("blog.index", _external=True))
            ]
        }
    }

