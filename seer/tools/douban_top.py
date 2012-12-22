# -*- coding: utf-8 -*-

import hammock
import string
from itertools import izip

from pyquery import PyQuery as pq

from seer.application import db
from seer.models.douban import DoubanTopMovie, DoubanMovie
from seer.models.mapping import Mapping

API_KEY = '06d9d6d0a87af3ca148d8471f970db5e'

FUNC_ENCODE_UTF8 = lambda x: x.encode('utf-8')
FUNC_EXTRACT_ID = lambda x: x.split('/')[-2]

def get_douban_top250_movies():
    url = 'http://movie.douban.com/top250?format=text'
    d = pq(url=url)
    item_trs = d('div.article table.list_view tbody tr.item')#[14:15]
    info_trs = d('div.article table.list_view tbody tr.info')#[14:15]

    db.session.query(DoubanTopMovie).delete()

    arg = lambda: None
    def _gen():
        for item_tr, info_tr in izip(item_trs, info_trs):
            item_tds = item_tr.findall('td')
            rank_td = item_tds[0]
            name_td = item_tds[1]
            rating_td = item_tds[2]
            rate_num_td = item_tds[3]

            arg.rank = rank_td.text.strip()
            arg.name = name_td.find('a').text.strip()
            _url = name_td.find('a').attrib['href']
            arg.douban_movie_id = FUNC_EXTRACT_ID(_url)
            arg.year = name_td.find('span').text.strip()
            arg.rating = rating_td.find('em').text.strip()
            arg.rate_num = rate_num_td.text.strip()

            info_td = info_tr.find('td')
            _meta = pq(info_td.find('p')).html()
            arg.credits, arg.region = map(string.strip, tuple(_meta.split('<br/>')))
            tip_p = pq(info_td).find('p').eq(1)
            arg.tip = tip_p.text().strip() if tip_p else ''

            r = get_movie_info(arg.douban_movie_id)
            if r.status_code == 200:
                info = r.json
                arg.pic_url = info['image']

            for k, v in arg.__dict__.iteritems():
                setattr(arg, k, FUNC_ENCODE_UTF8(v))

            yield arg

    for arg in _gen():
        print arg.name, arg.tip
        movie = DoubanTopMovie(**arg.__dict__)
        db.session.add(movie)

        db.session.commit()

    print 'done.'

def update_mapped_douban_movies():
    mapped_movie_ids = db.session.query(Mapping.douban_movie_id).all()
    mapped_movie_ids = [FUNC_ENCODE_UTF8(x[0]) for x in mapped_movie_ids]
    print len(mapped_movie_ids), 'movies to be updated...'
    for movie_id in mapped_movie_ids:
        update_movie_info(movie_id)

def get_movie_info(movie_id):
    client = hammock.Hammock('https://api.douban.com')
    return client.v2.movie(movie_id).GET(
            params=dict(
                apikey=API_KEY,
                )
            )

def update_movie_info(movie_id):
    db.session.query(DoubanMovie) \
            .filter(DoubanMovie.douban_movie_id==movie_id) \
            .delete()

    r = get_movie_info(movie_id)

    if r.status_code == 200:
        arg = lambda: None
        info = r.json
        arg.douban_movie_id = movie_id
        arg.name = FUNC_ENCODE_UTF8(info['title'])
        arg.rating = info['rating']['average']
        arg.rate_num = info['rating']['numRaters']
        arg.pic_url = info['image']

        print arg.douban_movie_id, arg.name, arg.rating, arg.rate_num
        movie = DoubanMovie(**arg.__dict__)
        db.session.add(movie)

        db.session.commit()
