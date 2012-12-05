#!/usr/bin/env python
# -*- coding: utf-8 -*-

import difflib
import hammock
import re
from operator import itemgetter

from seer.application import db
from seer.helper import normallize_name, unique
from seer.models.mapping import Mapping
from seer.models.program import Program
from seer.models.channel import Channel

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
        infos = r.json['movies']
        for i in infos:
            title = i['title'].encode('utf8')
            sid = i['id']
            sid = extract_id(sid)
            alt_title = i['alt_title'].encode('utf8')
            rating_num = i['rating']['numRaters']
            movie_tuples.append((title, sid, rating_num))
            alt_titles = alt_title.split('/')
            for at in alt_titles:
                at = at.strip()
                movie_tuples.append((at, sid, rating_num))

        movie_tuples = map(lambda x: x+(diff_ratio(name, x[0]),), movie_tuples)
        movie_tuples = filter(lambda x: x[3] > 0.5, movie_tuples)
        movie_tuples = sorted(movie_tuples,
                key=itemgetter(3, 2),
                reverse=True)

    # title, id, rating_num, ratio
    return movie_tuples

def get_matching_sid(name):
    movie_tuples = match_name(name)
    if movie_tuples:

        for title, sid, rating_num, ratio in movie_tuples:
            print title, sid, rating_num, ratio

        title, sid, rating_num, ratio = movie_tuples[0]
        return sid

def get_unresolved_normalized_names():
    resolved_names = get_resolved_normalized_names()
    all_names = get_all_normalized_names()
    return list(set(all_names) - set(resolved_names))

def get_resolved_normalized_names():
    results = db.session.query(Mapping.name).all()
    names = [r[0] for r in results]
    names = [n.encode('utf8') for n in names]
    return names

def get_all_names(priority_threshold=9):
    channels = db.session.query(Channel) \
            .filter(Channel.priority>=priority_threshold).all()
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
        sid = get_matching_sid(n)
        if sid:
            m = Mapping(
                    name=n,
                    sid=sid,
                    )
            db.session.add(m)
            db.session.commit()
            print 'Mapping: ', n, '=>', sid
