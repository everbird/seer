# -*- coding: utf-8 -*-

from seer.extensions import db
from seer.helper import gen_repr


class DoubanTopMovie(db.Model):
    __tablename__ = 'douban_top_movie'
    __table_args__ = (
            db.UniqueConstraint('douban_movie_id', 'rank'),
            dict(
                mysql_engine='InnoDB',
                mysql_charset='utf8',
            ))

    id = db.Column(db.Integer, primary_key=True)
    douban_movie_id = db.Column(db.Unicode(20), nullable=False)
    name = db.Column(db.Unicode(200), server_default='', nullable=False)
    rating = db.Column(db.Unicode(10), server_default='')
    rate_num = db.Column(db.Integer)
    rank = db.Column(db.Integer)
    year = db.Column(db.Integer)
    credits = db.Column(db.Unicode(200), server_default='')
    region = db.Column(db.Unicode(200), server_default='')
    tip = db.Column(db.Unicode(200), server_default='')

    __repr__ = gen_repr(props=['name', 'douban_movie_id', 'rank'])
