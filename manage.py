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
def drop_all_immeditely():
    """ Drops all database tables immeditely
    """
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

@manager.option('-c', '--channel', help='Channel id')
def fetch_kandianshi(channel):
    return watchdog.fetch_kandianshi(channel)

@manager.option('-c', '--channel', help='Channel id')
@manager.option('-n', '--datenum', help='Date number')
def fetch_tvmao(channel, datenum):
    return watchdog.fetch_tvmao(channel, datenum)

@manager.command
def fetch_all():
    return watchdog.fetch_all()

@manager.command
def init_db():
    return watchdog.init_db()

@manager.option('-n', '--datenum', help='Date number')
@manager.option('-d', '--days', help='Days count', default=7, type=int)
def online(datenum, days):
    return watchdog.do_online(datenum, days)

@manager.command
def mapping():
    return watchdog.do_mapping()

@manager.command
def apply():
    return watchdog.do_apply()

@manager.command
def douban_top():
    return watchdog.do_douban_top()

@manager.command
def update_douban():
    return watchdog.do_update_douban()

@manager.option('-n', '--datenum', help='Date number to package.')
@manager.option('-t', '--target', help='Target package path.')
@manager.option('-d', '--days', help='Days count from specifed datenum.',
        default=1, type=int)
def package(target, datenum, days):
    watchdog.do_package(target, datenum, days)

manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
