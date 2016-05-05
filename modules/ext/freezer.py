from flask.ext.frozen import Freezer

from application import app
from modules.ext.helpers import get_data

freezer = Freezer(app)


@freezer.register_generator
def blog_post():
    for slug in get_data("blog").keys():
        yield ("blog.post", {"slug": slug})
