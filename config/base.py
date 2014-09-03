import markdown
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

	MD = None
	MD_OPTIONS = {
		"output_format": "html5",

		"extensions": [
			"toc",
			"extra",
			"smarty",
			"modules.video",
			"modules.absoluter",
			#"meta",
			#"codehilite"
		],

		"extension_configs":{
			"toc": [
				("anchorlink", True),
				("slugify", lambda s, sep: pytils.translit.slugify(s)),
			],

			"modules.absoluter": [
				("base_url", lambda: url_for("blog.index", _external=True))
			]
		}
	}

	def __init__(self):
		self.MD = markdown.Markdown(**self.MD_OPTIONS)


