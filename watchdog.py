#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errno
import os
import subprocess
from config import config

from seer.tools import fetch, init_channels, online


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
    for c, name in init_channels.CHANNEL_DATA.iteritems():
        print 'feching %s: %s' % (c, name)
        fetch_tvmao(c)
        fetch_kandianshi(c)

def do_online():
    online.online()
