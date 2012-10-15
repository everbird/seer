#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_admin.contrib import sqlamodel

from seer import views
from seer.config import DefaultConfig
from seer.extensions import db, admin
from seer.models.program import Program

__all__ = ['create_app']

DEFAULT_APP_NAME = "seer"

DEFAULT_MODULES = (
    (views.frontend, ""),
)

def create_app(config=None, app_name=None, modules=None):
    if app_name is None:
        app_name = DEFAULT_APP_NAME
    if modules is None:
        modules = DEFAULT_MODULES
    app = Flask(app_name)

    configure_app(app, config)

    configure_extensions(app)
    configure_modules(app, modules)

    return app

def configure_app(app, config):
    app.config.from_object(DefaultConfig())
    if config is not None:
        app.config.from_object(config)
    app.config.from_envvar('APP_CONFIG', silent=True)

def configure_extensions(app):
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    db.init_app(app)
    admin.add_view(sqlamodel.ModelView(Program, db.session))
    #admin.add_view(sqlamodel.GalleryManager(name='Name', category='Cats'))
    admin.init_app(app)

def configure_modules(app, modules):
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)
