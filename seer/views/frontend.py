#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Module, render_template

from seer.models.program import Program

frontend = Module(__name__)

@frontend.route('/')
def index():
    return 'ok'

@frontend.route('/win8/privacy_policy')
def win8_privacy_plicy():
    return render_template('privacy_prolicy.jade')

@frontend.route('/hot')
def hot_programs():
    top250_movies = Program.query.get_top_programs()
    mapped_movies = Program.query.get_mapped_programs()
    return render_template('hot.jade', **locals())
