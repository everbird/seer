# seer.models.channel
# -*- coding: utf-8 -*-


from seer.extensions import db
from seer.helper import gen_repr


class Channel(db.Model):
    __tablename__ = 'channel'
    __table_args__ = (
            dict(
                mysql_engine='InnoDB',
                mysql_charset='utf8',
            ))

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), server_default='', nullable=False)
    priority = db.Column(db.Integer)
    programs = db.relationship('Program', backref='channel', lazy='dynamic')
    external = db.relationship('External', backref='channel', uselist=False)

    __repr__ = gen_repr(props=['id', 'name'])

    def __unicode__(self):
        return self.name
