# tools.fetch-programs-kandianshi
# -*- coding: utf-8 -*-

import datetime
import sys
from os.path import dirname, abspath
seer_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, seer_path)

from pyquery import PyQuery as pq

from seer.application import db
from seer.models.program import Program

FUNC_ENCODE_UTF8 = lambda x: x.encode('utf-8')


def kandianshi(channel, datenum=None):
    year1900 = datetime.datetime(1900, 1, 1)
    t = datetime.datetime.today()
    today = datetime.datetime(t.year, t.month, t.day)
    datenum = datenum or today.strftime('%Y%m%d')
    url_pattern = 'http://www.kandianshi.com/%d_%s'
    url=url_pattern % (channel, datenum)
    print 'connecting:', url
    d = pq(url=url)

    print 'deleting old data...'
    db.session.query(Program).filter_by(channel_id=channel).delete()
    db.session.commit()

    trs = d('#zhongbu table table tr')
    for tr in trs[1:]:
        tds = tr.findall('td')
        if len(tds)==3:
            _start, _name, _length = list(map(FUNC_ENCODE_UTF8,
                [x.text for x in tds]))
            _time = datetime.datetime.strptime(_start, '%H:%M')
            delta = _time - year1900
            start = today + delta
            name = _name.strip()
            length = _length.replace('分钟', '').strip()
            datenum = int(start.strftime('%Y%m%d'))

            print start, name, length
            p = Program(
                    start_dt=start,
                    name=name,
                    length=length,
                    channel_id=channel,
                    datenum=datenum)
            db.session.add(p)
            db.session.commit()

    print 'done.'
