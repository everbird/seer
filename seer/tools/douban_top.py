# -*- coding: utf-8 -*-

import string
from itertools import izip

from pyquery import PyQuery as pq

from seer.application import db
from seer.models.douban import DoubanTopMovie

FUNC_ENCODE_UTF8 = lambda x: x.encode('utf-8')
FUNC_EXTRACT_ID = lambda x: x.split('/')[-2]

def get_douban_top250_movies():
    url = 'http://movie.douban.com/top250?format=text'
    d = pq(url=url)
    item_trs = d('div.article table.list_view tbody tr.item')#[14:15]
    info_trs = d('div.article table.list_view tbody tr.info')#[14:15]

    db.session.query(DoubanTopMovie).delete()

    print d.html().encode('utf8')
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

            for k, v in arg.__dict__.iteritems():
                setattr(arg, k, FUNC_ENCODE_UTF8(v))

            yield arg

    for arg in _gen():
        print arg.name, arg.tip
        movie = DoubanTopMovie(**arg.__dict__)
        db.session.add(movie)

        db.session.commit()

    print 'done.'
