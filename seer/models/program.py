# seer.models.program
# -*- coding: utf-8 -*-

from datetime import datetime

from flask_sqlalchemy import BaseQuery

from seer.extensions import db
from seer.helper import DateTime, gen_repr
from seer.models.extra import ProgramExtra


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
