#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_admin import Admin, AdminIndexView, expose
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from flask_redis import Redis
from flask_cache import Cache
from flask_bootstrap import Bootstrap

from seer.decorators import requires_auth

__all__ = ['db', 'admin', 'manager', 'redis', 'cache', 'boostrap']

class AuthAdminHome(AdminIndexView):
    @expose('/')
    @requires_auth
    def index(self):
        return self.render('admin_index.html')

db = SQLAlchemy()
admin = Admin(name='Admin of Seer', index_view=AuthAdminHome())
manager = APIManager()
redis = Redis()
cache = Cache()
bootstrap = Bootstrap()
