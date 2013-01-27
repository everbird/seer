# -*- coding: utf-8 -*-


from datetime import datetime

from seer.helper import DateTime, gen_repr
from seer.extensions import db

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = (
            db.UniqueConstraint('douban_id'),
            dict(
                mysql_engine='InnoDB',
                mysql_charset='utf8',
            ))

    id = db.Column(db.Integer, primary_key=True)
    douban_id = db.Column(db.Unicode(100), nullable=False)
    name = db.Column(db.Unicode(100), server_default='', nullable=False)
    update_dt = db.Column(DateTime, default=datetime.now)
    access_token = db.Column(db.Unicode(100), nullable=False)

    __repr__ = gen_repr(props=['id', 'name', 'douban_id'])

    def __unicode__(self):
        return self.name
