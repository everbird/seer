#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import Flask, request
from flask_admin.contrib import sqlamodel, fileadmin

from configs import config

from seer import views
from seer.config import DefaultConfig

try:
    from seer.local_config import DefaultConfig
except ImportError, e:
    if e.args[0].startswith('No module named local_config'):
        pass
    else:
        # the ImportError is raised inside local_config
        raise

from seer.extensions import db, admin, manager, bootstrap
from seer.models.program import Program
from seer.models.channel import Channel
from seer.models.candidate import Candidate, CandidateProgram
from seer.models.external import External
from seer.models.mapping import Mapping
from seer.models.extra import ProgramExtra
from seer.models.douban import DoubanTopMovie, DoubanMovie
from seer.models.user import User, UserDevice

__all__ = ['create_app']

DEFAULT_APP_NAME = "seer"

DEFAULT_MODULES = (
    (views.frontend, ""),
    (views.api, "/api")
)

def create_app(config=None, app_name=None, modules=None):
    if app_name is None:
        app_name = DEFAULT_APP_NAME
    if modules is None:
        modules = DEFAULT_MODULES
    app = Flask(app_name)

    configure_app(app, config)

    configure_statics(app)
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
    bootstrap.init_app(app)

    def check_auth(username, password):
        return username == 'admin' and password == 'secret'

    class AuthFileAdmin(fileadmin.FileAdmin):

        def is_accessible(self):
            auth = request.authorization
            return auth and check_auth(auth.username, auth.password)


    def _make_model_view(model_class, *args, **kwargs):

        class AuthModelView(sqlamodel.ModelView):

            def is_accessible(self):
                auth = request.authorization
                return auth and check_auth(auth.username, auth.password)

        return AuthModelView(model_class, db.session, *args, **kwargs)

    admin.add_view(_make_model_view(Program, endpoint='program',
        category='Online'))
    admin.add_view(_make_model_view(Channel, endpoint='channel',
        category='Online'))
    admin.add_view(_make_model_view(CandidateProgram,
        endpoint='candidate_programe', category='Backend'))
    admin.add_view(_make_model_view(Candidate, endpoint='candidate',
        category='Backend'))
    admin.add_view(_make_model_view(External, endpoint='external',
        category='Backend'))
    admin.add_view(_make_model_view(Mapping, endpoint='mapping',
        category='Mapping'))
    admin.add_view(_make_model_view(ProgramExtra, endpoint='program_extra',
        category='Backend'))
    admin.add_view(_make_model_view(DoubanTopMovie,
        endpoint='douban_top_movie', category='Mapping'))
    admin.add_view(_make_model_view(DoubanMovie, endpoint='douban_movie',
        category='Mapping'))
    admin.add_view(_make_model_view(User,
        endpoint='user', category='User'))
    admin.add_view(_make_model_view(UserDevice,
        endpoint='user_device', category='User'))

    path = os.path.join(config.VAR_PATH, config.SITE_PORT,
            config.PACKAGE_FILES_PATH)
    admin.add_view(AuthFileAdmin(path, '/packages/', endpoint='packages',
        name='Package Files'))
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
    manager.create_api(User, methods=['GET', 'POST', 'PUT', 'PATCH'])
    manager.create_api(UserDevice, methods=['GET', 'POST', 'PUT', 'PATCH'])

def configure_statics(app):
    if app.config['DEBUG']:
        from configs import config as conf
        from os import path
        from werkzeug.wsgi import SharedDataMiddleware
        package_path = path.join(conf.VAR_PATH, conf.SITE_PORT, 'www', 'packages')
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/packages': path.join(package_path, 'www', 'packages')
            })
