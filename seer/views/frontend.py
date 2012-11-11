#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Module, render_template


frontend = Module(__name__)

@frontend.route('/')
def index():
    return 'ok'

@frontend.route('/win8/privacy_policy')
def win8_privacy_plicy():
    return render_template('privacy_prolicy.jade')
