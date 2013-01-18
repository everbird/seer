#!/usr/bin/env python
# -*- coding: utf8 -*-

import komandr
import os
import sys
from itertools import chain
from os.path import join, dirname, abspath, isfile
from string import Template

src = dirname(abspath(__file__))

ENV_GENERATE_FILES = {
        'dev': {
            'configs/templates/supervisord.conf.template': 'supervisord.conf',
            'configs/templates/local_config.py.template': 'configs/local_config.py',
            'configs/templates/seer_local_config.py.template': 'seer/local_config.py',
            'configs/templates/redis-store.conf.template': 'redis-store.conf',
            'configs/templates/redis-cache.conf.template': 'redis-cache.conf',
            },
        'product': {
            'configs/templates/supervisord.conf.template': 'supervisord.conf',
            'configs/templates/redis-store.conf.template': 'redis-store.conf',
            'configs/templates/redis-cache.conf.template': 'redis-cache.conf',
            }
        }

def _generate(env, config):
    for source, target in ENV_GENERATE_FILES[env].iteritems():

        # Generate by generate_stacks
        with open(join(src, source)) as f:
            content = Template(f.read())\
                    .substitute(**config.__dict__)
            with open(join(src, target), 'w') as o:
                o.write(content)
                print target, 'generated.'

@komandr.command
def dev():
    from configs.templates import config
    _generate('dev', config)
    print 'Development config files done.'

@komandr.command
def product():
    from configs import config
    _generate('product', config)
    print 'Production config files done.'

@komandr.command
def clean():
    fnames = chain.from_iterable(i.values() for i in ENV_GENERATE_FILES.values())
    for fname in fnames:
        fpath = join(src, fname)

        if isfile(fpath):
            os.remove(fpath)
            print fname, 'removed.'
        else:
            print fname, 'not exist.'

@komandr.command
def _command():
    dev()

if __name__ == '__main__':
    komandr.main() if sys.argv[1:] else dev()
