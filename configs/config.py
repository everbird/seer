#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

DEVELOP_MODE = True
PROJECT_NAME = 'seer'
PROJECT_DIR = '/home/everbird/code/%s' % PROJECT_NAME
SITE_PORT = '8100'
SITE_DOMAIN = 'seer.everbird.net'
SITE_HOME = 'http://%s:%s' %(SITE_DOMAIN, SITE_PORT)
SHOWN_HOME = 'http://%s' % SITE_DOMAIN

REDIS_STORE_HOST = 'localhost'
REDIS_STORE_PORT = 6379

REDIS_CACHE_HOST = 'localhost'
REDIS_CACHE_PORT = 7379

PACKAGE_FILES_PATH = 'www/packages'
VAR_PATH = '/home/everbird/var'
VAR_DIRS = ['log',
            'run',
            'tmp',
            'data/redis/store',
            'data/redis/cache',
            PACKAGE_FILES_PATH,
            ]

try:
    from local_config import *
except ImportError, e:
    if e.args[0].startswith('No module named local_config'):
        pass
    else:
        # the ImportError is raised inside local_config
        raise

logfile = os.path.expanduser('%s/%s/log/%s-output.log' % \
        (VAR_PATH, SITE_PORT, PROJECT_NAME))

def setup_logs():
    try:
        debug_log = open(logfile, 'a', 1)
        sys.stdout = debug_log
    except (IOError, OSError), exc:
        sys.stderr.write('error open debug log %r: %s\n'
                % (logfile, exc.strerror))
