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

    # --- Bootstrap ---
    BOOTSTRAP_USE_MINIFIED = True
    BOOTSTRAP_USE_CDN = True
    BOOTSTRAP_FONTAWESOME = True
    SECRET_KEY = 'devkey'
    RECAPTCHA_PUBLIC_KEY = 'fake'
