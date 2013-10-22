import markdown
import pytils

class Config(object):
	DEBUG = True

	FREEZER_BASE_URL = "http://www.mindcollapse.com/"
	FREEZER_REMOVE_EXTRA_FILES = True
	FREEZER_DESTINATION = "build"
	FREEZER_DESTINATION_IGNORE = [
		".git*", 
		".ht*", 
		"robots.txt", 
		"favicon.ico",
	]

	MD = None
	MD_OPTIONS = {
		"output_format": "html5",

		"extensions": [
			"toc",
			"extra",
			"meta"
		],

		"extension_configs":{
			"toc": [
				("anchorlink", True),
				("slugify", lambda s, sep: pytils.translit.slugify(s)),
			]
		}
	}

	def __init__(self):
		self.MD = markdown.Markdown(**self.MD_OPTIONS)


