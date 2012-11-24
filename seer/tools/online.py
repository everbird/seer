# seer.tools.online
# -*- coding: utf-8 -*-

import sys
from os.path import dirname, abspath
seer_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, seer_path)

from seer.application import db
from seer.models.channel import Channel
from seer.models.candidate import CandidateProgram
from seer.models.program import Program

def online():
    channels = db.session.query(Channel).all()
    for channel in channels:
        print 'Updating:', channel.name.encode('utf8'),
        db.session.query(Program)\
                .filter_by(channel_id=channel.id)\
                .delete()

        cp = db.session.query(CandidateProgram) \
                .filter(CandidateProgram.channel_id==channel.id) \
                .order_by(CandidateProgram.candidate_id) \
                .first()

        if not cp:
            print 'no candidate program for ', channel.name.encode('utf8')
            continue

        candidate = cp.candidate
        print 'using:', candidate.name.encode('utf8')
        channel.programs = [p.as_program()
                for p in candidate.candidate_programs
                if p.channel_id==channel.id]
        db.session.add(channel)

    db.session.commit()
