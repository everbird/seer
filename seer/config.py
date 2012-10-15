#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DefaultConfig(object):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql://seer:burning@localhost/seer_d"
    SQLALCHEMY_ECHO = False
