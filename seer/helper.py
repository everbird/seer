# seer.helper
# -*- coding: utf-8 -*-

"""
Helper, or the one who need help
"""


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
