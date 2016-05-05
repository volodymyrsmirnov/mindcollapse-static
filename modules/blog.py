import datetime
import markdown

from flask import current_app, Response, url_for, redirect, render_template, Blueprint, abort
from flask.ext.assets import Environment
from webassets.script import CommandLineEnvironment

from modules.ext.helpers import get_data, get_content, hyphenate

from assets import blog_js_bundle, blog_css_bundle

blog = Blueprint("blog", __name__)


def process_post(entry, content=True, hyphens=True):
    processed_post = {
        "slug": entry[0],
        "date": entry[1],
        "title": entry[2],
        "file": entry[3],
        "type": entry[4],

        "parsed_date": datetime.datetime.strptime(entry[1], "%Y-%m-%d"),
    }

    if content:
        processed_post["raw_content"] = get_content("blog", processed_post["file"])

        if processed_post["type"] == "html":
            processed_post["content"] = processed_post["raw_content"]

        elif processed_post["type"] == "markdown":
            markdown_converter = markdown.Markdown(**current_app.config["MD_OPTIONS"])

            processed_post["content"] = markdown_converter.reset().convert(processed_post["raw_content"])

            # noinspection PyUnresolvedReferences
            processed_post["first_image"] = markdown_converter.first_image

        if hyphens:
            processed_post["content"] = hyphenate(processed_post["content"])

    return processed_post


@blog.before_app_first_request
def register_assets():
    assets = Environment(current_app)
    assets.register("blog_js", blog_js_bundle)
    assets.register("blog_css", blog_css_bundle)

    CommandLineEnvironment(assets, current_app.logger).build()


@blog.route("/nginx_redirect.conf")
def nginx_redirect():
    return Response(
        "return 307 {0};".format(url_for("blog.post", slug=list(get_data("blog").items())[0][0], _external=True)),
        mimetype="text/plain"
    )


@blog.route("/")
def index():
    return redirect(url_for("blog.post", slug=list(get_data("blog").items())[0][0]))


@blog.route("/404.html")
def error_404():
    return render_template("blog/404.html")


@blog.route("/blog/archive/")
def archive():
    return render_template(
        "blog/archive.html", posts=[process_post(p, content=False) for p in list(get_data("blog").values())]
    )


@blog.route("/blog/<slug>.html")
def post(slug):
    entries = get_data("blog")

    if slug not in entries:
        return abort(404)

    entries_keys = list(entries.keys())

    next_slug = entries_keys[entries_keys.index(slug) + 1] if slug != entries_keys[-1] else None
    prev_slug = entries_keys[entries_keys.index(slug) - 1] if slug != entries_keys[0] else None

    return render_template("blog/post.html", post=process_post(entries[slug]), next_slug=next_slug, prev_slug=prev_slug)


@blog.route("/blog.xml")
def rss():
    return Response(render_template(
        "blog/rss.xml", posts=[process_post(p, hyphens=False) for p in list(get_data("blog").values())[0:8]]
    ), mimetype="application/xml")


@blog.route("/blog/sitemap.xml")
def sitemap():
    return Response(render_template(
        "blog/sitemap.xml", posts=[process_post(p, content=False) for p in list(get_data("blog").values())]
    ), mimetype="application/xml")
