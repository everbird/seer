#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from flask_script import Manager, prompt_bool

from seer import create_app
from seer.extensions import db

import watchdog

manager = Manager(create_app)

@manager.command
def create_all():
    """ Creates database tables
    """
    db.create_all()

@manager.command
def drop_all():
    """ Drops all database tables
    """
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

@manager.command
def version():
    """ Output current version
    """
    print watchdog.version()

@manager.command
def var_dir():
    """ Output the directory path for current project in var
    """
    print watchdog.var_dir()

@manager.command
def build_var():
    """ Initialize var dir for deployment
    """
    watchdog.build_var()

@manager.shell
def make_shell_context():
    return dict(app=current_app)

@manager.option('-n', '--channel', help='Channel id')
def fetch_kandianshi(channel):
    return watchdog.fetch_kandianshi(channel)

manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
