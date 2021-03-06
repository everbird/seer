# seer.models.external
# -*- coding: utf-8 -*-


from seer.extensions import db
from seer.helper import gen_repr


class External(db.Model):
    __tablename__ = 'channel_external'
    __table_args__ = (
            dict(
                mysql_engine='InnDB',
                mysql_charset='utf8',
            ))

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    kandianshi_id = db.Column(db.Integer)
    tvmao_tv_id = db.Column(db.String(100))
    tvmao_channel_id = db.Column(db.String(100))

    __repr__ = gen_repr(props=['id', 'channel_id', 'kandianshi_id',
        'tvmao_channel_id'])

    def __unicode__(self):
        return self.channel_id
