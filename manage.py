#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from flaskext.script import Manager

from seer import create_app

import watchdog

manager = Manager(create_app)

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
def build_playground():
    """ Initialize the playground dirs for results and logs
    """
    watchdog.build_playground()

@manager.command
def build_var():
    """ Initialize var dir for deployment
    """
    watchdog.build_var()

@manager.shell
def make_shell_context():
    return dict(app=current_app)

manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
