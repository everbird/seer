#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errno
import os
import subprocess
from config import config

from seer.tools import fetch, init_channels, online, match, douban_top


def version():
    cmd = 'git describe'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output = p.communicate()[0].strip()
    return output

def var_dir():
    return os.path.expanduser('~/var/%s' % config.SITE_PORT)

def build_var():
    for dname in config.VAR_DIRS:
        dpath = os.path.join(config.VAR_PATH, config.SITE_PORT, dname)
        _mkdir(dpath)

def _mkdir(path):
    if not os.path.isdir(path):
        mkdir_p(path)
        print path,'dir created.'
    else:
        print path, 'existed.'

def mkdir_p(path):
    """ 'mkdir -p' in Python
    """
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise

def build_playground():
    _mkdir(config.PLAYGROUND_PATH)

    dirs = [config.QUEUE_PATH,
            config.COLLECTION_PATH,
            config.TMP_PATH,
            config.WORKERS_PATH,
            config.LOG_PATH,
            ]
    for dpath in dirs:
        _mkdir(dpath)

    logfiles = [config.PICKLOG_PATH,
            config.EXPORTLOG_PATH,
            config.NEWLIB_PATH,
            ]
    for fpath in logfiles:
        if not os.path.isfile(fpath):
            open(fpath, 'w').close()
            print fpath, 'file touched.'

    for w in config.WORKERS:
        wpath = os.path.join(config.WORKERS_PATH, w)
        _mkdir(wpath)
        for wd in config.WORKER_DIRS:
            _mkdir(os.path.join(wpath, wd))

def fetch_kandianshi(channel):
    return fetch.kandianshi(int(channel))

def fetch_tvmao(channel):
    return fetch.tvmao(int(channel))

def init_db():
    init_channels.init()

def fetch_all():
    for c, (name, priority) in init_channels.CHANNEL_DATA.iteritems():
        print 'feching %s: %s' % (c, name), priority
        fetch_tvmao(c)
        fetch_kandianshi(c)

def do_online():
    online.online()

def do_mapping():
    match.update_unresolved_names()

def do_apply():
    match.apply()

def do_douban_top():
    douban_top.get_douban_top250_movies()

def do_update_douban():
    douban_top.update_mapped_douban_movies()
