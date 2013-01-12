#!/usr/bin/env python
# -*- coding: utf8 -*-

from os.path import join, dirname, abspath
from string import Template

from templates import config

def run():
    src = dirname(dirname(abspath(__file__)))

    generate_stacks = {
            'configs/templates/supervisord.conf.template': 'supervisord.conf',
            'configs/templates/local_config.py.template': 'configs/local_config.py',
            'configs/templates/seer_local_config.py.template': 'seer/local_config.py',
            }
    for source, target in generate_stacks.iteritems():

        # Generate by generate_stacks
        with open(join(src, source)) as f:
            content = Template(f.read())\
                    .substitute(**config.__dict__)
            with open(join(src, target), 'w') as o:
                o.write(content)
                print target, 'generated.'

    print 'done.'



if __name__ == '__main__':
    run()
