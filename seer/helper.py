# seer.helper
# -*- coding: utf-8 -*-

"""
Helper, or the one who need help
"""

import re

def iunique(iterable):
    seen = set()
    for i in iterable:
        if i not in seen:
            seen.add(i)
            yield i

def unique(iterable):return list(iunique(iterable))

# Gist from https://gist.github.com/1080563
# Monkey patch to use UTC+8 timezone
import pytz
from sqlalchemy.types import TypeDecorator
from sqlalchemy import DateTime as SdateTime
tz = pytz.timezone('Asia/Shanghai')
class DateTime(TypeDecorator):
    impl = SdateTime

    def process_bind_param(self, value, engine):
        return value

    def process_result_value(self, value, engine):
        return tz.localize(value)

def get_repr(obj, props=None, trailing=''):
    props = props or []
    valid_types = (str, unicode, int, long)

    def func_print(obj, p):
        x = getattr(obj, p, '')
        return x.encode('utf8') if isinstance(x, (str, unicode)) else x

    func_format = lambda o, x: \
            '%s="%s"' % (x, func_print(o, x))
    props_repr = ', '.join([func_format(obj, p)
        for p in props \
                if hasattr(obj, p) \
                and isinstance(getattr(obj, p), valid_types)])
    return '<%s %s %s>' % (obj.__class__.__name__, props_repr,
            trailing)

def gen_repr(props=None, trailing=''):
    def f(obj):
        return get_repr(obj, props=props, trailing=trailing)
    return f

def normallize_name(name):
    name = name.replace('回看 ', '')
    _name = re.sub(r'(故事片|译制片|系列片|录播|首播|专题|回看|黄金剧场|直播中|直播|电视剧|电影)(:|：)(.*)', r'\3', name)
    trim_words = ['重播', '字幕']
    for w in trim_words:
        _name = re.sub(r'(.*?)(\(\%(word)s\)|（\%(word)s）)(.*$)' % {'word': w},
                r'\1\3', _name)
    cleaned_name = _name
    _name = _name.strip()
    _name = re.sub(r'(.*?)(\d+/\d+)(.*$)', r'\1\3', _name)
    _name = _name.strip()
    m = re.search(r'(\d+)$', cleaned_name)
    _trailing = m.group() if m else ''
    _name = re.sub(r'(\d+)', r'-', _name)
    _name = re.sub(r'-$', r'%s'%_trailing, _name)
    _name = _name.strip()
    _name = re.sub(r'(.*?)(\(\-\)|（\-）)(.*$)', r'\1\3', _name)
    _name = re.sub(r'(\(|（)([^\)]*)(\)|）)', r'', _name)
    _name = _name.strip()

    ignore_words = ['光影星播客', '世界电影之旅', '电影报道', '爱电影',
            '电影情报站', '形象片', '电影频道梦工场', '垫播', '电影人物',
            '爱上电影网', '佳片有约', '光影周刊', '世界纪录电影长廊',
            '首映庆典', '片场直击']
    for w in ignore_words:
        if w in _name:
            return ''

    return _name

to_utf8 = lambda x: x.encode('utf8')

def trunc(s, max_len=40, etc='...'):
    s = str(s).decode("utf-8")
    if len(s)>= max_len:
        s = s[:max_len] + str(etc)
    return s.encode("utf-8")
