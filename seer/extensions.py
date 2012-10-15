#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

__all__ = ['db']

db = SQLAlchemy()
admin = Admin()
