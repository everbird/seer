# seer.tools.online
# -*- coding: utf-8 -*-

import sys
from os.path import dirname, abspath
seer_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, seer_path)

from seer.application import db
from seer.models.channel import Channel
from seer.models.candidate import CandidateProgram

def online():
    channels = db.session.query(Channel).all()
    for channel in channels:
        cp = db.session.query(CandidateProgram) \
                .filter(CandidateProgram.channel_id==channel.id) \
                .order_by(CandidateProgram.candidate_id) \
                .first()

        if not cp:
            continue

        candidate = cp.candidate
        channel.programs = [p.as_program()
                for p in candidate.candidate_programs
                if p.channel_id==channel.id]
        db.session.add(channel)

    db.session.commit()
