import datetime

import flask

from flask.ext.assets import Environment
from webassets.script import CommandLineEnvironment

from assets import blog_js_bundle, blog_css_bundle

from modules.helpers import get_data, get_content, hyphenate

blog = flask.Blueprint("blog", __name__)

def process_post(entry, content=True, hyphens=True):
    post = {}

    post["slug"], post["date"], post["title"], post["file"], post["type"] = entry
    post["parsed_date"] = datetime.datetime.strptime(post["date"], "%Y-%m-%d")
    
    if content:
        post["raw_content"] = get_content("blog", post["file"])

        if post["type"] == "html": 
            post["content"] = post["raw_content"]

        elif post["type"] == "markdown": 
            post["content"] = flask.current_app.config["MD"].reset().convert(post["raw_content"]) 
            post["first_image"] = flask.current_app.config["MD"].first_image

        if hyphens:
            post["content"] = hyphenate(post["content"])

    return post

@blog.before_app_first_request
def register_assets():
    assets = Environment(flask.current_app)
    assets.register("blog_js", blog_js_bundle)
    assets.register("blog_css", blog_css_bundle)

    cmdenv = CommandLineEnvironment(assets, flask.current_app.logger)
    cmdenv.build()

@blog.route("/nginx_redirect.conf")
def nginx_redirect():
    first_post = get_data("blog").items()[0]

    response = flask.make_response("return 307 {0}".format((flask.url_for("blog.post", slug=first_post[0], _external=True))))
    response.headers["Content-Type"] = "text/plain"
    return response

@blog.route("/")
def index():
    return ""

@blog.route("/404.html")
def error_404():
    return flask.render_template("blog/404.html")

@blog.route("/blog/archive/")
def archive():
    posts = []

    for entry in get_data("blog").items():
        post = {}
        post["slug"], post["date"], post["title"], post["file"], post["type"] = entry[1]
        post["parsed_date"] = datetime.datetime.strptime(post["date"], "%Y-%m-%d")

        posts.append(post)

    return flask.render_template("blog/archive.html", posts=posts)
    
@blog.route("/blog/<slug>.html")
def post(slug):
    entries = get_data("blog")

    if not slug in entries:
        return flask.abort(404)

    next_slug = None
    prev_slug = None

    entries_keys = entries.keys()
    current_slug_index = entries_keys.index(slug)

    if not slug == entries_keys[-1]:
        next_slug = entries_keys[current_slug_index + 1]

    if not slug == entries_keys[0]:
        prev_slug = entries_keys[current_slug_index - 1]   

    return flask.render_template("blog/post.html", post=process_post(entries[slug]), next_slug=next_slug, prev_slug=prev_slug)

@blog.route("/blog.xml")
def rss():
    posts = []

    for post in get_data("blog").values()[0:8]:
        posts.append(process_post(post, hyphens=False))

    response = flask.make_response(flask.render_template("blog/rss.xml", posts=posts))
    response.headers["Content-Type"] = "application/xml"
    return response

@blog.route("/blog/sitemap.xml")
def sitemap():
    posts = []

    for post in get_data("blog").values():
        posts.append(process_post(post, content=False))

    response = flask.make_response(flask.render_template("blog/sitemap.xml", posts=posts))
    response.headers["Content-Type"] = "application/xml"
    return response