# -*- coding: utf-8 -*-

from seer.extensions import db
from seer.helper import gen_repr

class Mapping(db.Model):
    __tablename__ = 'mapping'
    __table_args__ = (
            db.UniqueConstraint('name', 'sid'),
            dict(
                mysql_engine='InnoDB',
                mysql_charset='utf8',
            ))

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), server_default='', nullable=False)
    sid = db.Column(db.Unicode(20), nullable=False)

    __repr__ = gen_repr(props=['name', 'sid'])
