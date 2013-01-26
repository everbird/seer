# -*- coding: utf-8 -*-

from flask import Module, jsonify

from seer.views.helper import program_entry
from seer.models.program import Program

api = Module(__name__)

@api.route('/chart')
def chart():
    top250_movies = Program.query.get_top_programs()
    rating_movies = Program.query.get_mapped_programs()

    return jsonify(
            top250=[program_entry(p) for p in top250_movies],
            rating=[program_entry(p) for p in rating_movies],
    )
