# -*- coding: utf-8 -*-

from seer.extensions import db
from seer.helper import gen_repr

class ProgramExtra(db.Model):
    __tablename__ = 'program_extra'
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

    def __unicode__(self):
        return self.name
