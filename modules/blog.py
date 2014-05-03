import datetime

import flask

from flask.ext.assets import Environment
from webassets.script import CommandLineEnvironment

from assets import blog_js_bundle, blog_css_bundle

from modules.helpers import get_data, get_content, hyphenate

blog = flask.Blueprint("blog", __name__)

def process_post(entry, content=True, hyphens=True):
    post = {
        "slug": entry[0],
        "date": entry[1],
        "title": entry[2],
        "file": entry[3],
        "type": entry[4],
        "parsed_date": datetime.datetime.strptime(entry[1], "%Y-%m-%d"),
    }

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

    CommandLineEnvironment(assets, flask.current_app.logger).build()

@blog.route("/nginx_redirect.conf")
def nginx_redirect():
    return flask.Response(
        "return 307 {0};".format(
            flask.url_for(
                "blog.post", 
                slug=get_data("blog").items()[0][0], 
                _external=True
            )
        ),
        mimetype="text/plain"
    )

@blog.route("/")
def index():
    return flask.redirect(
        flask.url_for(
            "blog.post", 
            slug=get_data("blog").items()[0][0]
        )
    )

@blog.route("/404.html")
def error_404():
    return flask.render_template(
        "blog/404.html"
    )

@blog.route("/blog/archive/")
def archive():
    posts = [
        {
            "slug": entry[1][0],
            "date": entry[1][1],
            "title": entry[1][2],
            "file": entry[1][3],
            "type": entry[1][4],
            "parsed_date": datetime.datetime.strptime(entry[1][1], "%Y-%m-%d"),

        } for entry in get_data("blog").items()
    ]

    return flask.render_template(
        "blog/archive.html", 
        posts=posts
    )
    
@blog.route("/blog/<slug>.html")
def post(slug):
    entries = get_data("blog")

    entries_keys = entries.keys()

    next_slug = entries_keys[entries_keys.index(slug) + 1] if slug != entries_keys[-1] else None
    prev_slug = entries_keys[entries_keys.index(slug) - 1] if slug != entries_keys[0] else None

    return flask.render_template(
        "blog/post.html", 
        post=process_post(entries[slug]), 
        next_slug=next_slug, 
        prev_slug=prev_slug
    )

@blog.route("/blog.xml")
def rss():
    posts = [
        process_post(post, hyphens=False) for post in get_data("blog").values()[0:8]
    ]

    return flask.Response(
        flask.render_template("blog/rss.xml", posts=posts),
        mimetype="application/xml"
    )

@blog.route("/blog/sitemap.xml")
def sitemap():
    posts = [
        process_post(post, content=False) for post in get_data("blog").values()
    ]

    return flask.Response(
        flask.render_template("blog/sitemap.xml", posts=posts),
        mimetype="application/xml"
    )