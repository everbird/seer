# seer.models.candidate
# -*- coding: utf-8 -*-

import time
from datetime import datetime

from seer.extensions import db
from seer.models.channel import Channel
from seer.models.program import Program
from seer.helper import DateTime, gen_repr

K_CANDIDATE_KANDIANSHI = 'kandianshi'
K_CANDIDATE_TVMAO = 'tvmao'
CANDIDATE_NAMES = {
        K_CANDIDATE_KANDIANSHI: '看电视',
        K_CANDIDATE_TVMAO: '电视猫',
        }

# high => low
CANDIDATE_PRIORITY = [
        K_CANDIDATE_TVMAO,
        K_CANDIDATE_KANDIANSHI,
        ]

class Candidate(db.Model):
    __tablename__ = 'candidate'
    __table_args__ = (
            dict(
                mysql_engine='InnoDB',
                mysql_charset='utf8',
            ))

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), nullable=True)
    name = db.Column(db.Unicode(100), server_default='', nullable=False)
    candidate_programs = db.relationship('CandidateProgram',
            backref='candidate',
            lazy='dynamic')
    programs = db.relationship('Program',
            backref='candidate',
            lazy='dynamic')

    __repr__ = gen_repr(props=['uid', 'name'])

    def __unicode__(self):
        return self.name


class CandidateProgram(db.Model):
    __tablename__ = 'candidate_program'
    __table_args__ = (
            db.UniqueConstraint('channel_id', 'candidate_id', 'start_dt'),
            dict(
                mysql_engine='InnoDB',
                mysql_charset='utf8',
            ))

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    name = db.Column(db.Unicode(100), server_default='', nullable=False)
    length = db.Column(db.Integer)
    datenum = db.Column(db.Integer, nullable=False)
    start_dt = db.Column(DateTime, default=datetime.now)
    update_dt = db.Column(DateTime, default=datetime.now)
    end_dt = db.Column(DateTime, default=datetime.now)

    __repr__ = gen_repr(props=['id', 'name', 'channel_id'])

    def __unicode__(self):
        return self.name

    @property
    def channel(self):
        return db.session.query(Channel).filter(Channel.id==self.channel_id)

    def as_program(self):
        delta = (self.start_dt - datetime(1970, 1, 1,
            tzinfo=self.start_dt.tzinfo))
        total_secs = delta.total_seconds()
        pid = '%s-%s-%s' % (self.datenum, self.channel_id,
                hex(int(total_secs)))
        return Program(
                pid=pid,
                name=self.name,
                length=self.length,
                datenum=self.datenum,
                start_dt=self.start_dt,
                update_dt=self.update_dt,
                end_dt=self.end_dt,
                channel_id=self.channel_id,
                candidate_id=self.candidate_id
                )
