# -*- coding: utf-8 -*-

from seer.extensions import db
from seer.helper import gen_repr
from seer.models.douban import DoubanTopMovie, DoubanMovie

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
    program_id = db.Column(db.Integer, nullable=False)

    __repr__ = gen_repr(props=['name', 'douban_movie_id'])

    def __unicode__(self):
        return self.name

    @property
    def program(self):
        from seer.models.program import Program
        return db.session.query(Program) \
                .filter(Program.id==self.program_id) \
                .first()

    @property
    def douban_top_movie(self):
        return db.session.query(DoubanTopMovie) \
                .filter(DoubanTopMovie.douban_movie_id==self.douban_movie_id) \
                .first()

    @property
    def douban_mapped_movie(self):
        return db.session.query(DoubanMovie) \
                .filter(DoubanMovie.douban_movie_id==self.douban_movie_id) \
                .first()
