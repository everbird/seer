#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

DEVELOP_MODE = True
PROJECT_NAME = 'seer'
PROJECT_DIR = '/home/everbird/code/%s' % PROJECT_NAME
SITE_PORT = '8100'
VAR_PATH = os.path.expanduser('~/var')
logfile = os.path.expanduser('%s/%s/log/%s-output-%s.log' % \
        (VAR_PATH, SITE_PORT, PROJECT_NAME, SITE_PORT))

def setup_logs():
    try:
        debug_log = open(logfile, 'a', 1)
        sys.stdout = debug_log
    except (IOError, OSError), exc:
        sys.stderr.write('error open debug log %r: %s\n'
                % (logfile, exc.strerror))

VAR_DIRS = ['log',
            'run',
            'tmp',
            'www',
            ]

try:
    from local_config import *
except ImportError, e:
    if e.args[0].startswith('No module named local_config'):
        pass
    else:
        # the ImportError is raised inside local_config
        raise
