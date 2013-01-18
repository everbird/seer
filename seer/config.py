#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DefaultConfig(object):
    DEBUG = False
    SECRET_KEY = "secret"

    # --- SQLAlchemy ---
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://seer:burning@localhost/seer_d"
    SQLALCHEMY_ECHO = False

    # --- Redis ---
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
