# seer.models.program
# -*- coding: utf-8 -*-

from datetime import datetime

from flask_sqlalchemy import BaseQuery

from seer.extensions import db
from seer.helper import DateTime, gen_repr
from seer.models.extra import ProgramExtra
from seer.models.douban import DoubanTopMovie as Top, DoubanMovie


class ProgramQuery(BaseQuery):

    def as_list(self):
        deferred_cols = (
                'channel_id',
                'start_dt',
                )
        options = [db.defer(col) for col in deferred_cols]
        return self.options(*options)

    def search(self, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(Program.name.ilike(keyword),
                ))
        q = reduce(db.and_, criteria)
        return self.filter(q).distinct()

    def get_top_programs(self, show_all=False):
        exp = db.session.query(Program) \
                .filter(ProgramExtra.douban_movie_id==Top.douban_movie_id) \
                .filter(Program.extra_id==ProgramExtra.id)

        if not show_all:
            exp = exp.filter(Program.datenum>=datetime.now().strftime('%Y%m%d'))

        return exp.all()

    def get_mapped_programs(self,
            rating_threshold=7,
            rate_num_threshold=100,
            show_all=False):
        exp = db.session.query(Program) \
                .filter(db.and_(
                    Program.extra_id==ProgramExtra.id,
                    ProgramExtra.douban_movie_id==DoubanMovie.douban_movie_id,
                    DoubanMovie.rating>=rating_threshold,
                    DoubanMovie.rate_num>=rate_num_threshold))

        if not show_all:
            exp = exp.filter(Program.datenum>=datetime.now().strftime('%Y%m%d'))

        return exp.all()


class Program(db.Model):
    __tablename__ = 'program'
    __table_args__ = (
            db.UniqueConstraint('channel_id', 'start_dt'),
            dict(
                mysql_engine='InnoDB',
                mysql_charset='utf8',
            ))

    query_class = ProgramQuery

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    name = db.Column(db.Unicode(100), server_default='', nullable=False)
    length = db.Column(db.Integer)
    datenum = db.Column(db.Integer, nullable=False)
    start_dt = db.Column(DateTime, default=datetime.now)
    update_dt = db.Column(DateTime, default=datetime.now)
    end_dt = db.Column(DateTime, default=datetime.now)
    extra_id = db.Column(db.Integer, db.ForeignKey(ProgramExtra.id))
    extra = db.relationship(ProgramExtra, uselist=False)

    __repr__ = gen_repr(props=['id', 'name', 'channel_id'])

    def __unicode__(self):
        return self.name

    def exist_one(self):
        return db.session.query(Program)\
                .filter_by(channel_id=self.channel_id)\
                .filter_by(start_dt=self.start_dt)\
                .first()

    def conflict_programs(self):
        return db.session.query(Program)\
                .filter_by(channel_id=self.channel_id)\
                .filter(db.or_(
                    db.and_(Program.start_dt<self.start_dt, Program.end_dt>self.start_dt),
                    db.and_(Program.start_dt<self.end_dt, Program.end_dt>self.end_dt)
                    ))\
                .all()
