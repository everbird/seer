#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

from seer import views
from seer.config import DefaultConfig

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
    configure_before_handlers(app)
    configure_template_filters(app)
    configure_modules(app, modules)

    return app

def configure_app(app, config):
    app.config.from_object(DefaultConfig())
    if config is not None:
        app.config.from_object(config)
    app.config.from_envvar('APP_CONFIG', silent=True)

def configure_extensions(app):
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    pass

def configure_modules(app, modules):
    for module, url_prefix in modules:
        #app.register_module(module, url_prefix=url_prefix)
        app.register_blueprint(module, url_prefix=url_prefix)

def configure_before_handlers(app):
    pass

def configure_template_filters(app):
    pass
