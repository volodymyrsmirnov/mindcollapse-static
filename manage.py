#!/usr/bin/env python

from flask.ext.script import Manager

from application import app
from freezer import freezer

manager = Manager(app)

@manager.command
def freeze():
	freezer.freeze()

if __name__ == "__main__":
    manager.run()