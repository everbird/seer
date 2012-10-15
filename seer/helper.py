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
