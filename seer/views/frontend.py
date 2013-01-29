#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict, OrderedDict

from flask import Module, render_template as rt

from seer.models.program import Program

frontend = Module(__name__)

@frontend.route('/')
def index():
    return 'ok'

@frontend.route('/win8/privacy_policy')
def win8_privacy_plicy():
    return rt('privacy_prolicy.jade')

@frontend.route('/hot')
@frontend.route('/douban/hot')
def hot_programs():
    top250_movies = Program.query.get_top_programs()
    mapped_movies = Program.query.get_mapped_programs()
    _id_programs = {}
    program_categories = defaultdict(list)
    for p in mapped_movies:
        _id_programs[p.id] = p
        program_categories[p.id].append('rating')

    for p in top250_movies:
        _id_programs[p.id] = p
        program_categories[p.id].append('top250')

    id_programs = OrderedDict(sorted(_id_programs.items(),
        key=lambda x: x[1].start_dt))

    return rt('hot.jade', **locals())

@frontend.route('/douban/all')
def douban_programs():
    mapped_movies = Program.query.get_mapped_programs(rating_threshold=0,
            rate_num_threshold=0)
    return rt('all.jade', **locals())
