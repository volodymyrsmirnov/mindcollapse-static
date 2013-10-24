import flask
import pytils
import datetime

from config.base import Config

from modules.blog import blog as blog_module

app = flask.Flask(__name__)
app.config.from_object(Config())

app.register_blueprint(blog_module)

@app.context_processor
def context_processor():
    return {
        "active": flask.request.endpoint,
        "pytils": pytils,
    }