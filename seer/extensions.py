#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from flask_redis import Redis
from flask_cache import Cache

__all__ = ['db', 'admin', 'manager', 'redis', 'cache']

db = SQLAlchemy()
admin = Admin()
manager = APIManager()
redis = Redis()
cache = Cache()
