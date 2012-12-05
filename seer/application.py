#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_admin.contrib import sqlamodel

from seer import views
from seer.config import DefaultConfig
from seer.extensions import db, admin, manager
from seer.models.program import Program
from seer.models.channel import Channel
from seer.models.candidate import Candidate, CandidateProgram
from seer.models.external import External
from seer.models.mapping import Mapping

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
    admin.add_view(sqlamodel.ModelView(Channel, db.session))
    admin.add_view(sqlamodel.ModelView(CandidateProgram, db.session))
    admin.add_view(sqlamodel.ModelView(Candidate, db.session))
    admin.add_view(sqlamodel.ModelView(External, db.session))
    admin.add_view(sqlamodel.ModelView(Mapping, db.session))
    admin.init_app(app)
    manager.init_app(app, flask_sqlalchemy_db=db)
    configure_api(manager)

def configure_modules(app, modules):
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)

def configure_api(manager):
    manager.create_api(Program, methods=['GET'], results_per_page=None)
    manager.create_api(Channel, methods=['GET'], results_per_page=None,
            exclude_columns=['programs', 'external', 'candidate',
                'candidate_id'])
