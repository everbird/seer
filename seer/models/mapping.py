# -*- coding: utf-8 -*-

from seer.extensions import db
from seer.helper import gen_repr, to_utf8

class Mapping(db.Model):
    __tablename__ = 'mapping'
    __table_args__ = (
            db.UniqueConstraint('name', 'douban_movie_id'),
            dict(
                mysql_engine='InnoDB',
                mysql_charset='utf8',
            ))

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), server_default='', nullable=False)
    douban_movie_id = db.Column(db.Unicode(20), nullable=False)

    __repr__ = gen_repr(props=['name', 'douban_movie_id'])


def get_mapping():
    mappings = db.session.query(Mapping.name, Mapping.douban_movie_id).all()
    return dict([map(to_utf8, x) for x in mappings])
