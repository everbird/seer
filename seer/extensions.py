#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

__all__ = ['db', 'admin', 'manager']

db = SQLAlchemy()
admin = Admin()
manager = APIManager()
