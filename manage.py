#!/usr/bin/env python

from application import app
from flask.ext.script import Manager
from modules.ext.freezer import freezer

manager = Manager(app)


@manager.command
def freeze():
    freezer.freeze()


if __name__ == "__main__":
    manager.run()
