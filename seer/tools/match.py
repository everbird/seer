#!/usr/bin/env python
# -*- coding: utf-8 -*-

import difflib
import hammock
import re
import time
from operator import itemgetter

from seer.application import db
from seer.helper import normallize_name, unique
from seer.models.mapping import Mapping, get_mapping
from seer.models.program import Program
from seer.models.channel import Channel
from seer.models.extra import ProgramExtra

API_KEY = '06d9d6d0a87af3ca148d8471f970db5e'

def extract_id(url):
    m = re.search(r'movie/(\d+)', url)
    return m.group(1) if m else ''

def diff_ratio(source, target):
    return difflib.SequenceMatcher(None, source, target).ratio()

def match_name(name):
    client = hammock.Hammock('https://api.douban.com')
    r = client.v2.movie.search.GET(
            params=dict(
                q=name,
                apikey=API_KEY,
                )
            )

    movie_tuples = []
    if r.status_code == 200:
        infos = r.json['subjects']
        for i in infos:
            douban_movie_id = i['id']
            sr = client.v2.movie.subject(douban_movie_id).GET(
                    params=dict(apikey=API_KEY)
                    )
            time.sleep(0.2)
            info = sr.json
            title = info.get('title', '').encode('utf8')
            alt_titles = info.get('aka', [])
            rating_num = info.get('ratings_count', 0)
            movie_tuples.append((title, douban_movie_id, rating_num))
            alt_titles = map(lambda x: x.encode('utf8'), alt_titles)
            for at in alt_titles:
                at = at.strip()
                movie_tuples.append((at, douban_movie_id, rating_num))

        movie_tuples = map(
                lambda x: x+(diff_ratio(name, x[0]), diff_ratio(x[0], name)),
                movie_tuples)
        movie_tuples = filter(lambda x: x[3] >= 0.6 and x[4] >= 0.6,
                movie_tuples)
        movie_tuples = sorted(movie_tuples,
                key=itemgetter(3, 2),
                reverse=True)
    else:
        print r.status_code, r.content

    # title, id, rating_num, ratio
    return movie_tuples

def get_matching_douban_movie_id(name):
    movie_tuples = match_name(name)
    print 'map:', name, len(movie_tuples)
    if movie_tuples:

        for title, douban_movie_id, rating_num, ratio, ratio_r in movie_tuples:
            print title, douban_movie_id, rating_num, ratio, ratio_r

        title, douban_movie_id, rating_num, ratio, ratio_r = movie_tuples[0]
        return douban_movie_id

def get_unresolved_normalized_names():
    resolved_names = get_resolved_normalized_names()
    all_names = get_all_normalized_names()
    return list(set(all_names) - set(resolved_names))

def get_resolved_normalized_names():
    results = db.session.query(Mapping.name).all()
    names = [r[0] for r in results]
    names = [n.encode('utf8') for n in names]
    return names

def get_channels(priority_threshold=9):
    return db.session.query(Channel) \
            .filter(Channel.priority>=priority_threshold).all()

def get_all_names():
    channels = get_channels()
    results = []
    for ch in channels:
        _ = db.session.query(Program.name) \
                .filter(Program.channel_id==ch.id).all()
        results += _
    names = [r[0] for r in results]
    names = [n.encode('utf8') for n in names]
    return names

def get_all_normalized_names():
    names = get_all_names()
    names = unique([normallize_name(n) for n in names])
    names = [n for n in names if n]
    return names


def update_unresolved_names():
    names = get_unresolved_normalized_names()
    for n in names:
        douban_movie_id = get_matching_douban_movie_id(n)
        if douban_movie_id:
            m = Mapping(
                    name=n,
                    douban_movie_id=douban_movie_id,
                    )
            db.session.add(m)
            db.session.commit()
            print 'Mapping: ', n, '=>', douban_movie_id

def apply_mapping(mapping):
    channels = get_channels()
    for channel in channels:
        for p in channel.programs:
            name = normallize_name(p.name.encode('utf8'))
            matched_douban_movie_id = mapping.get(name)
            if matched_douban_movie_id:
                exist = db.session.query(ProgramExtra) \
                        .filter(ProgramExtra.name==name) \
                        .filter(ProgramExtra.douban_movie_id==matched_douban_movie_id) \
                        .first()
                if not exist:
                    print 'apply %s to %s' % (matched_douban_movie_id, p)
                    extra = ProgramExtra(
                            name=name,
                            douban_movie_id=matched_douban_movie_id,
                            program_id=p.id,
                            )
                    p.extra = extra
                    db.session.add(extra)
                    db.session.add(p)
                else:
                    print 'exist:', name, matched_douban_movie_id
            db.session.commit()
            print channel, 'applied'


def apply():
    mappings = get_mapping()
    apply_mapping(mappings)

    print 'done'
