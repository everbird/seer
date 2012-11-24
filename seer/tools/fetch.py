# seer.tools.fetch
# -*- coding: utf-8 -*-

import datetime
import sys
from os.path import dirname, abspath
seer_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, seer_path)

import requests
from pyquery import PyQuery as pq

from seer.application import db
from seer.models.candidate import CandidateProgram, Candidate
from seer.models.channel import Channel

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

    candidate = db.session.query(Candidate)\
            .filter(Candidate.uid=='kandianshi').one()

    print 'deleting old data...'
    db.session.query(CandidateProgram)\
            .filter_by(channel_id=channel, candidate_id=candidate.id)\
            .delete()
    db.session.commit()

    trs = d('#zhongbu table table tr')
    def _gen():
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
                length = int(length) if length.isdigit() else 0
                during = datetime.timedelta(minutes=length)
                end = start + during
                datenum = int(start.strftime('%Y%m%d'))

                yield name, datenum, start, end, length

    for name, datenum, start, end, length in _gen():
        print start, name, length
        cp = CandidateProgram(
                candidate=candidate,
                start_dt=start,
                end_dt=end,
                name=name,
                length=length,
                channel_id=channel,
                datenum=datenum)
        db.session.add(cp)

        db.session.commit()

    print 'done.'

def tvmao(channel, datenum=None):
    year1900 = datetime.datetime(1900, 1, 1)
    t = datetime.datetime.today()
    today = datetime.datetime(t.year, t.month, t.day)
    datenum = datenum or today.strftime('%Y%m%d')
    url_pattern = 'http://www.tvmao.com/ext/show_tv.jsp?p=%s&c=%s'
    ch = db.session.query(Channel).filter(Channel.id==channel).first()
    if not ch:
        print 'Channel: %s not exist.' % channel
        return

    ext = ch.external
    url=url_pattern % (ext.tvmao_tv_id, ext.tvmao_channel_id)
    print 'connecting:', url

    # Using requests to avoid strange encoding issue of pyquery
    r = requests.get(url)
    d = pq(r.text)

    candidate = db.session.query(Candidate)\
            .filter(Candidate.uid=='tvmao').one()

    print 'deleting old data...'
    db.session.query(CandidateProgram)\
            .filter_by(channel_id=channel, candidate_id=candidate.id)\
            .delete()
    db.session.commit()

    lis = d('.pgmain div.epg #pgrow li')
    end = None
    def _gen():
        for li in lis:
            if pq(li).attr('id') in ('noon', 'night'):
                continue

            _start = FUNC_ENCODE_UTF8(li.find('span').text)
            _time = datetime.datetime.strptime(_start, '%H:%M')
            delta = _time - year1900
            start = today + delta
            datenum = int(start.strftime('%Y%m%d'))

            pq(li).find('.green_line,.drama,span.am,span.pm,span.nt').remove()
            pq(li).children().filter(lambda x: pq(this).text() == u'在线观看').remove()

            _name = FUNC_ENCODE_UTF8(pq(li).text())
            name = _name.strip()
            yield start, name, datenum

    datas = list(_gen())
    start_datas = [d[0] for d in datas]
    end_datas = start_datas[1:] + [today+datetime.timedelta(days=1)]
    for (start, name, datenum), end in zip(datas, end_datas):
        delta = (end - start)
        length = delta.seconds / 60

        print start, end, name, datenum, length
        cp = CandidateProgram(
                candidate=candidate,
                start_dt=start,
                end_dt=end,
                name=name,
                length=length,
                channel_id=channel,
                datenum=datenum)
        db.session.add(cp)

        db.session.commit()

    print 'done.'
