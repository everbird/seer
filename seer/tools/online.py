# seer.tools.online
# -*- coding: utf-8 -*-

import sys
from os.path import dirname, abspath
seer_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, seer_path)

from seer.application import db
from seer.models.channel import Channel
from seer.models.candidate import Candidate, CandidateProgram
from seer.models.program import Program

def online():
    channels = db.session.query(Channel).all()
    for channel in channels:
        online_by_channel(channel)


def online_by_channel(channel):
    print 'Updating:', channel.name.encode('utf8'),
    db.session.query(Program)\
            .filter_by(channel_id=channel.id)\
            .delete()

    candidates = db.session.query(Candidate) \
            .order_by(Candidate.id) \
            .all()

    programs = get_programs(candidates, channel.id)

    if not programs:
        print 'no candidate program for ', channel.name.encode('utf8')

    channel.programs = programs

    db.session.add(channel)
    db.session.commit()

def get_programs(candidates, channel_id):
    programs = []
    for c in candidates:
        try:
            cps = db.session.query(CandidateProgram) \
                    .filter(CandidateProgram.channel_id==channel_id,
                            CandidateProgram.candidate_id==c.id).all()
            programs = [p.as_program() for p in cps]
        except UnicodeDecodeError as e:
            print e

        if programs:
            print 'using', c.name.encode('utf8')
            break

    return programs
