#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DefaultConfig(object):
    DEBUG = True
    SECRET_KEY = "secret"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://seer:burning@localhost/seer_d"
    SQLALCHEMY_ECHO = False
