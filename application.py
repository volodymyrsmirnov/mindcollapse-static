import flask

from config.base import Config

from modules.blog import blog as blog_module
from modules.ext.helpers import no_shy

app = flask.Flask(__name__)
app.config.from_object(Config())
app.register_blueprint(blog_module)
app.jinja_env.filters["no_shy"] = no_shy


@app.context_processor
def context_processor():
    return {"active": flask.request.endpoint}
