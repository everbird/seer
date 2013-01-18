#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from flask_redis import Redis

__all__ = ['db', 'admin', 'manager', 'redis']

db = SQLAlchemy()
admin = Admin()
manager = APIManager()
redis = Redis()
